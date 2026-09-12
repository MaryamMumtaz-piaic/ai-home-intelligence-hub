from app.agents._shared import normalize_recommendations, room_name_lookup, run_agent

SYSTEM_PROMPT = (
    "You are the Accessibility Agent inside a home-intelligence system. Analyze room layout, "
    "movement paths, furniture placement, doors/hallways, and any stated accessibility needs. "
    "Recommendations that require a professional accessibility assessment must be flagged as "
    "such. Respond with JSON: {\"observations\": [string], \"recommendations\": [recommendation "
    "objects]}. Each recommendation object has: title, category ('accessibility'), room_id, "
    "room_name, priority, why_it_matters, recommended_action, expected_benefit, effort, "
    "estimated_cost {type,min,max,currency,is_estimate}, confidence, assumptions, "
    "requires_professional_assessment."
)


def analyze(home: dict) -> dict:
    lifestyle = home.get("lifestyle") or {}
    if not lifestyle.get("has_accessibility_considerations"):
        rooms = home.get("rooms") or []
        payload_rooms = rooms
    else:
        payload_rooms = home.get("rooms") or []
    if not payload_rooms:
        return {"observations": [], "recommendations": [], "succeeded": True, "error": None}
    payload = {
        "rooms": [
            {
                "id": r.get("id"),
                "name": r.get("name"),
                "type": r.get("room_type"),
                "door_count": r.get("door_count"),
                "problems": r.get("current_problems"),
                "furniture_blocking_movement": [
                    f.get("name") for f in (r.get("furniture") or []) if f.get("blocks_movement")
                ],
            }
            for r in payload_rooms
        ],
        "accessibility_notes": lifestyle.get("accessibility_notes"),
        "has_accessibility_considerations": lifestyle.get("has_accessibility_considerations", False),
    }
    result = run_agent("accessibility", SYSTEM_PROMPT, payload, ["observations", "recommendations"])
    result["recommendations"] = normalize_recommendations(
        result.get("recommendations", []), "accessibility", room_name_lookup(home)
    )
    return result
