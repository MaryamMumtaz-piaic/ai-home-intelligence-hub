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


def normalize_recommendations(raw: list, category: str, room_lookup: dict) -> list[dict]:
    """Cleans a raw list of model-produced recommendation dicts into the exact
    recommendation-shaped dict used across the app, filling safe defaults for any
    missing field so a partially-formed model response never crashes downstream code."""
    cleaned = []
    if not isinstance(raw, list):
        return cleaned
    for item in raw:
        if not isinstance(item, dict):
            continue
        room_id = item.get("room_id")
        room_name = item.get("room_name") or room_lookup.get(room_id)
        cost = item.get("estimated_cost") or {}
        cleaned.append(
            {
                "title": str(item.get("title") or "Untitled recommendation")[:200],
                "category": item.get("category") or category,
                "room_id": room_id,
                "room_name": room_name,
                "priority": item.get("priority") or "medium",
                "why_it_matters": str(item.get("why_it_matters") or "")[:1000] or "Not specified.",
                "recommended_action": str(item.get("recommended_action") or "")[:1000] or "Not specified.",
                "expected_benefit": str(item.get("expected_benefit") or "")[:500] or "Potential improvement.",
                "effort": item.get("effort") or "medium",
                "estimated_cost": {
                    "type": cost.get("type", "none"),
                    "min": cost.get("min", 0) or 0,
                    "max": cost.get("max", 0) or 0,
                    "currency": cost.get("currency", "USD") or "USD",
                    "is_estimate": True,
                },
                "confidence": item.get("confidence") or "medium",
                "assumptions": item.get("assumptions") or [],
                "requires_professional_assessment": bool(item.get("requires_professional_assessment", False)),
            }
        )
    return cleaned


def room_name_lookup(home: dict) -> dict:
    return {r.get("id"): r.get("name") for r in (home.get("rooms") or []) if isinstance(r, dict)}
