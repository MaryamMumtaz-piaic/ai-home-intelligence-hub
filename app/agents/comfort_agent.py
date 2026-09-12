from app.agents._shared import normalize_recommendations, room_name_lookup, run_agent

SYSTEM_PROMPT = (
    "You are the Comfort Agent inside a home-intelligence system. Analyze natural light, room "
    "purpose, furniture layout, and user preferences to find comfort improvements: lighting, "
    "layout adjustments, ventilation, and noise reduction. Respond with JSON: "
    '{"observations": [string], "recommendations": [recommendation objects]}. Each recommendation '
    "object has: title, category ('comfort'), room_id, room_name, priority, why_it_matters, "
    "recommended_action, expected_benefit, effort, estimated_cost {type,min,max,currency,"
    "is_estimate}, confidence, assumptions, requires_professional_assessment."
)


def analyze(home: dict) -> dict:
    rooms = home.get("rooms") or []
    if not rooms:
        return {"observations": [], "recommendations": [], "succeeded": True, "error": None}
    payload = {
        "rooms": [
            {
                "id": r.get("id"),
                "name": r.get("name"),
                "type": r.get("room_type"),
                "natural_light": r.get("natural_light"),
                "window_count": r.get("window_count"),
                "problems": r.get("current_problems"),
                "preferred_style": r.get("preferred_style"),
            }
            for r in rooms
        ],
        "lifestyle": home.get("lifestyle"),
        "climate_zone_or_location": home.get("climate_zone_or_location"),
    }
    result = run_agent("comfort", SYSTEM_PROMPT, payload, ["observations", "recommendations"])
    result["recommendations"] = normalize_recommendations(
        result.get("recommendations", []), "comfort", room_name_lookup(home)
    )
    return result
