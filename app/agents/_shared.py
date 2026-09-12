"""Shared helpers for sub-agent modules: safe model invocation and recommendation shaping."""

import json

from app.services.openai_service import OpenAIServiceError, chat_json

SAFETY_RULES = (
    "Rules you must always follow: never invent exact savings, costs, or guarantees; "
    "label every numeric estimate as an estimate; use hedged language such as 'potential', "
    "'estimated', or 'possible'; never suggest dangerous, structural, electrical, or gas work "
    "be done without a qualified professional; use priority 'urgent_attention' only for a "
    "genuine safety or maintenance concern, never for an ordinary design preference; do not "
    "reveal your internal reasoning, only concise user-facing conclusions; respond with a "
    "single JSON object and nothing else."
)


def run_agent(agent_name: str, system_prompt: str, payload: dict, output_keys: list[str]) -> dict:
    """Calls the model with a JSON payload, returns the parsed result merged with
    succeeded/error bookkeeping. On failure, returns an empty-but-valid shape."""
    empty = {key: [] for key in output_keys}
    try:
        result = chat_json(
            system_prompt=f"{system_prompt}\n\n{SAFETY_RULES}",
            user_prompt=json.dumps(payload, ensure_ascii=False),
        )
        for key in output_keys:
            result.setdefault(key, [])
        result["succeeded"] = True
        result["error"] = None
        return result
    except OpenAIServiceError as exc:
        return {**empty, "succeeded": False, "error": str(exc)}


_VALID_CATEGORIES = {
    "space", "organization", "energy", "maintenance", "comfort", "safety", "accessibility", "improvement",
}
_VALID_PRIORITIES = {"low", "medium", "high", "urgent_attention"}
_VALID_EFFORTS = {"low", "medium", "high"}
_VALID_CONFIDENCE = {"low", "medium", "high"}
_VALID_COST_TYPES = {"none", "low", "medium", "high"}


def _enum_or_default(value, valid: set, default: str) -> str:
    """The model sometimes returns a free-text explanation instead of a bare enum value
    (e.g. "Low effort; involves installation of devices." instead of "low"). Falling back
    to a safe default here is what stands between a malformed model response and an
    unhandled Pydantic ValidationError crashing the request."""
    if isinstance(value, str) and value.strip().lower() in valid:
        return value.strip().lower()
    return default


def _as_string_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value if v]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def normalize_recommendations(raw: list, category: str, room_lookup: dict) -> list[dict]:
    """Cleans a raw list of model-produced recommendation dicts into the exact
    recommendation-shaped dict used across the app, filling safe defaults for any
    missing or malformed field so a partially-formed model response never crashes
    downstream code (including strict Pydantic enum/list validation)."""
    cleaned = []
    if not isinstance(raw, list):
        return cleaned
    for item in raw:
        if not isinstance(item, dict):
            continue
        room_id = item.get("room_id")
        room_id = room_id if isinstance(room_id, str) else None
        room_name = item.get("room_name") or room_lookup.get(room_id)
        cost = item.get("estimated_cost") if isinstance(item.get("estimated_cost"), dict) else {}
        cost_min = cost.get("min", 0)
        cost_max = cost.get("max", 0)
        cleaned.append(
            {
                "title": str(item.get("title") or "Untitled recommendation")[:200],
                "category": _enum_or_default(item.get("category"), _VALID_CATEGORIES, category),
                "room_id": room_id,
                "room_name": room_name,
                "priority": _enum_or_default(item.get("priority"), _VALID_PRIORITIES, "medium"),
                "why_it_matters": str(item.get("why_it_matters") or "")[:1000] or "Not specified.",
                "recommended_action": str(item.get("recommended_action") or "")[:1000] or "Not specified.",
                "expected_benefit": str(item.get("expected_benefit") or "")[:500] or "Potential improvement.",
                "effort": _enum_or_default(item.get("effort"), _VALID_EFFORTS, "medium"),
                "estimated_cost": {
                    "type": _enum_or_default(cost.get("type"), _VALID_COST_TYPES, "none"),
                    "min": cost_min if isinstance(cost_min, (int, float)) else 0,
                    "max": cost_max if isinstance(cost_max, (int, float)) else 0,
                    "currency": str(cost.get("currency") or "USD")[:8],
                    "is_estimate": True,
                },
                "confidence": _enum_or_default(item.get("confidence"), _VALID_CONFIDENCE, "medium"),
                "assumptions": _as_string_list(item.get("assumptions")),
                "requires_professional_assessment": bool(item.get("requires_professional_assessment", False)),
            }
        )
    return cleaned


def room_name_lookup(home: dict) -> dict:
    return {r.get("id"): r.get("name") for r in (home.get("rooms") or []) if isinstance(r, dict)}
