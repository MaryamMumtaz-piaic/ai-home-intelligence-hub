from app.agents._shared import normalize_recommendations, room_name_lookup, run_agent

SYSTEM_PROMPT = (
    "You are the Organization Agent inside a home-intelligence system. Analyze storage "
    "availability, room purpose, and furniture/storage units to find decluttering and storage "
    "opportunities. Respond with JSON: {\"organization_opportunities\": [string], "
    '"decluttering_sequence": [string], "recommendations": [recommendation objects]}. Each '
    "recommendation object has: title, category ('organization'), room_id, room_name, priority, "
    "why_it_matters, recommended_action, expected_benefit, effort, estimated_cost "
    "{type,min,max,currency,is_estimate}, confidence, assumptions, requires_professional_assessment."
)


def analyze(home: dict) -> dict:
    rooms = home.get("rooms") or []
    if not rooms:
        return {
            "organization_opportunities": [],
            "decluttering_sequence": [],
            "recommendations": [],
            "succeeded": True,
            "error": None,
        }
    payload = {
        "rooms": [
            {
                "id": r.get("id"),
                "name": r.get("name"),
                "type": r.get("room_type"),
                "purpose": r.get("primary_purpose"),
                "problems": r.get("current_problems"),
                "storage_furniture": [
                    f.get("category")
                    for f in (r.get("furniture") or [])
                    if f.get("category") in ("wardrobe", "cabinet", "bookshelf", "storage_box", "dresser")
                ],
            }
            for r in rooms
        ],
        "lifestyle": home.get("lifestyle"),
    }
    result = run_agent(
        "organization", SYSTEM_PROMPT, payload, ["organization_opportunities", "decluttering_sequence", "recommendations"]
    )
    result["recommendations"] = normalize_recommendations(
        result.get("recommendations", []), "organization", room_name_lookup(home)
    )
    return result
