from app.agents._shared import normalize_recommendations, room_name_lookup, run_agent

SYSTEM_PROMPT = (
    "You are the Space Planning Agent inside a home-intelligence system. Analyze room "
    "dimensions, furniture sizes/positions, and stated problems to find circulation issues, "
    "crowded or unused areas, and furniture-placement improvements. Respond with JSON: "
    '{"space_issues": [string], "recommendations": [recommendation objects]}. Each recommendation '
    "object has: title, category ('space'), room_id, room_name, priority "
    "('low'|'medium'|'high'|'urgent_attention'), why_it_matters, recommended_action, "
    "expected_benefit, effort ('low'|'medium'|'high'), estimated_cost "
    "{type,min,max,currency,is_estimate}, confidence ('low'|'medium'|'high'), assumptions "
    "(list of strings), requires_professional_assessment (bool). Do not claim exact "
    "architectural compliance."
)


def analyze(home: dict) -> dict:
    rooms = home.get("rooms") or []
    if not rooms:
        return {"space_issues": [], "recommendations": [], "succeeded": True, "error": None}
    payload = {
        "rooms": [
            {
                "id": r.get("id"),
                "name": r.get("name"),
                "type": r.get("room_type"),
                "length_m": r.get("length_m"),
                "width_m": r.get("width_m"),
                "problems": r.get("current_problems"),
                "furniture": [
                    {
                        "name": f.get("name"),
                        "category": f.get("category"),
                        "width": f.get("width"),
                        "depth": f.get("depth"),
                        "blocks_movement": f.get("blocks_movement"),
                        "can_be_moved": f.get("can_be_moved"),
                    }
                    for f in (r.get("furniture") or [])
                ],
            }
            for r in rooms
        ],
        "lifestyle": home.get("lifestyle"),
    }
    result = run_agent("space_planning", SYSTEM_PROMPT, payload, ["space_issues", "recommendations"])
    result["recommendations"] = normalize_recommendations(
        result.get("recommendations", []), "space", room_name_lookup(home)
    )
    return result
