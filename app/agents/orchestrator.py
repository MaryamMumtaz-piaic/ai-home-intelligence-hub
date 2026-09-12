"""Home Intelligence Orchestrator.

Coordinates the sub-agents, merges their recommendations through the critic and
priority agents, and assembles the structured results the API layer turns into a
HomeIntelligenceReport / RecommendationList / ScenarioComparison.
"""

from app.agents import (
    accessibility_agent,
    comfort_agent,
    critic_agent,
    energy_agent,
    home_validator,
    improvement_agent,
    maintenance_agent,
    organization_agent,
    priority_agent,
    safety_agent,
    space_planning_agent,
)
from app.agents._shared import normalize_recommendations, room_name_lookup, run_agent
from app.services.openai_service import OpenAIServiceError, chat_json

_ROOM_STATUS_LABELS = {
    True: "Needs attention",
    False: "Looking good",
}


def _status_from_recs(recs: list[dict], room_id: str, category_prefix: tuple[str, ...]) -> str:
    for rec in recs:
        if rec.get("room_id") == room_id and rec.get("category") in category_prefix and rec.get("priority") in (
            "high",
            "urgent_attention",
        ):
            return "Needs attention"
    for rec in recs:
        if rec.get("room_id") == room_id and rec.get("category") in category_prefix:
            return "Opportunities available"
    return "Looking good"


def _score_from_recs(recs_for_home: list[dict], category: str) -> tuple[int, str]:
    matching = [r for r in recs_for_home if r.get("category") == category]
    if not matching:
        return 80, "No significant issues detected from the information provided."
    urgent = sum(1 for r in matching if r.get("priority") == "urgent_attention")
    high = sum(1 for r in matching if r.get("priority") == "high")
    score = 90 - (urgent * 25) - (high * 12) - (len(matching) * 3)
    score = max(10, min(95, score))
    summary = f"{len(matching)} planning opportunit{'y' if len(matching) == 1 else 'ies'} identified in this area."
    return score, summary


def analyze_home(home: dict) -> dict:
    validation = home_validator.validate_home(home)
    rooms = home.get("rooms") or []
    lookup = room_name_lookup(home)

    sections = [
        ("space_planning", space_planning_agent.analyze(home)),
        ("organization", organization_agent.analyze(home)),
        ("energy", energy_agent.analyze(home)),
        ("maintenance", maintenance_agent.analyze(home)),
        ("comfort", comfort_agent.analyze(home)),
        ("safety", safety_agent.analyze(home)),
        ("accessibility", accessibility_agent.analyze(home)),
    ]

    all_recs: list[dict] = []
    agent_sections = []
    any_failed = False
    for name, result in sections:
        succeeded = result.get("succeeded", True)
        if not succeeded:
            any_failed = True
        agent_sections.append(
            {
                "agent": name,
                "succeeded": succeeded,
                "error": result.get("error"),
                "summary": None if not succeeded else f"{len(result.get('recommendations', []))} recommendation(s).",
            }
        )
        all_recs.extend(result.get("recommendations", []))

    all_recs = critic_agent.review(all_recs)
    plan = improvement_agent.build_plan(all_recs)
    all_recs = priority_agent.prioritize(all_recs)

    category_scores = []
    for category, label in [
        ("space", "Space"),
        ("organization", "Organization"),
        ("energy", "Energy"),
        ("maintenance", "Maintenance"),
        ("comfort", "Comfort"),
        ("safety", "Safety Awareness"),
        ("accessibility", "Accessibility"),
    ]:
        score, summary = _score_from_recs(all_recs, category)
        category_scores.append({"category": category, "score": score, "label": label, "summary": summary})

    room_summaries = []
    for room in rooms:
        rid = room.get("id")
        room_recs = [r for r in all_recs if r.get("room_id") == rid]
        room_summaries.append(
            {
                "room_id": rid,
                "room_name": room.get("name"),
                "observations": (
                    f"{len(room_recs)} recommendation(s) generated for this room."
                    if room_recs
                    else "No specific issues identified from the information provided."
                ),
                "top_recommendations": [r["title"] for r in room_recs[:3]],
                "space_status": _status_from_recs(all_recs, rid, ("space",)),
                "maintenance_status": _status_from_recs(all_recs, rid, ("maintenance",)),
                "organization_status": _status_from_recs(all_recs, rid, ("organization",)),
            }
        )

    return {
        "category_scores": category_scores,
        "top_actions": priority_agent.top_actions(all_recs),
        "quick_wins": plan["quick_wins"] or priority_agent.quick_wins(all_recs),
        "high_priority_issues": priority_agent.high_priority_issues(all_recs),
        "missing_information": validation["missing_information"],
        "suggested_next_step": (
            "Add more room and furniture details to improve the accuracy of your report."
            if not rooms
            else "Review your top actions and save the ones you'd like to track as tasks."
        ),
        "room_summaries": room_summaries,
        "agent_sections": agent_sections,
        "recommendations": all_recs,
        "partial": any_failed,
        "data_completeness_percent": validation["data_completeness_percent"],
    }


_ROOM_SYSTEM_PROMPT = (
    "You are analyzing a single room inside a home-intelligence system. Given only this room's "
    "data plus minimal home context (goals, lifestyle), identify space, organization, comfort, "
    "and maintenance observations. Respond with JSON: {\"observations\": string, \"space_status\": "
    'string, "maintenance_status": string, "organization_status": string, "recommendations": '
    "[recommendation objects]}. Each recommendation object has: title, category "
    "('space'|'organization'|'energy'|'maintenance'|'comfort'|'safety'|'accessibility'|"
    "'improvement'), room_id, room_name, priority, why_it_matters, recommended_action, "
    "expected_benefit, effort, estimated_cost {type,min,max,currency,is_estimate}, confidence, "
    "assumptions, requires_professional_assessment. Never invent exact savings or guarantees."
)


def analyze_room(home: dict, room_id: str) -> dict:
    room = next((r for r in (home.get("rooms") or []) if r.get("id") == room_id), None)
    if room is None:
        return {
            "observations": "Room not found.",
            "space_status": "Unknown",
            "maintenance_status": "Unknown",
            "organization_status": "Unknown",
            "recommendations": [],
            "succeeded": False,
            "error": "Room not found.",
        }
    payload = {
        "room": room,
        "home_goals": home.get("main_goals"),
        "lifestyle": home.get("lifestyle"),
    }
    result = run_agent(
        "room_analysis",
        _ROOM_SYSTEM_PROMPT,
        payload,
        ["recommendations"],
    )
    result.setdefault("observations", "Analysis unavailable.")
    result.setdefault("space_status", "Unknown")
    result.setdefault("maintenance_status", "Unknown")
    result.setdefault("organization_status", "Unknown")
    result["recommendations"] = normalize_recommendations(
        result.get("recommendations", []), "space", {room_id: room.get("name")}
    )
    return result


def generate_recommendations(home: dict, category: str | None = None, room_id: str | None = None) -> list[dict]:
    report = analyze_home(home)
    recs = report["recommendations"]
    if room_id:
        recs = [r for r in recs if r.get("room_id") == room_id]
    if category:
        recs = [r for r in recs if r.get("category") == category]
    return recs


_SCENARIO_SYSTEM_PROMPT = (
    "You are the What-If Scenario advisor inside a home-intelligence system. Given a room's data "
    "and a proposed change, describe the current state, the proposed change, potential benefits, "
    "possible trade-offs, an estimated effort level, affected rooms, and required follow-up "
    "actions. This is a planning simulation, not an exact architectural or engineering "
    "simulation — never claim otherwise. Respond with JSON: {\"current_state_summary\": string, "
    '"proposed_change_summary": string, "potential_benefits": [string], "possible_trade_offs": '
    '[string], "estimated_effort": string, "affected_rooms": [string], '
    '"required_follow_up_actions": [string]}.'
)


def compare_scenario(home: dict, room_id: str, scenario_type: str, description: str) -> dict:
    room = next((r for r in (home.get("rooms") or []) if r.get("id") == room_id), None)
    if room is None:
        return {
            "current_state_summary": "",
            "proposed_change_summary": "",
            "potential_benefits": [],
            "possible_trade_offs": [],
            "estimated_effort": "unknown",
            "affected_rooms": [],
            "required_follow_up_actions": [],
            "succeeded": False,
            "error": "Room not found.",
        }
    payload = {
        "room": room,
        "scenario_type": scenario_type,
        "description": description,
        "lifestyle": home.get("lifestyle"),
    }
    try:
        result = chat_json(system_prompt=_SCENARIO_SYSTEM_PROMPT, user_prompt=str(payload))
        result["succeeded"] = True
        result["error"] = None
        for key in (
            "potential_benefits",
            "possible_trade_offs",
            "affected_rooms",
            "required_follow_up_actions",
        ):
            result.setdefault(key, [])
        result.setdefault("current_state_summary", "")
        result.setdefault("proposed_change_summary", description)
        result.setdefault("estimated_effort", "medium")
        return result
    except OpenAIServiceError as exc:
        return {
            "current_state_summary": f"Current state of {room.get('name', 'this room')} based on your saved data.",
            "proposed_change_summary": description,
            "potential_benefits": [],
            "possible_trade_offs": [],
            "estimated_effort": "unknown",
            "affected_rooms": [room.get("name")] if room.get("name") else [],
            "required_follow_up_actions": [],
            "succeeded": False,
            "error": str(exc),
        }


def energy_insights(home: dict) -> list[dict]:
    return energy_agent.analyze(home).get("recommendations", [])


def maintenance_plan(home: dict, maintenance_items: list[dict] | None = None) -> list[dict]:
    return maintenance_agent.analyze(home, maintenance_items).get("recommendations", [])


def organization_plan(home: dict) -> list[dict]:
    return organization_agent.analyze(home).get("recommendations", [])
