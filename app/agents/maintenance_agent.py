from app.agents._shared import normalize_recommendations, room_name_lookup, run_agent

SYSTEM_PROMPT = (
    "You are the Maintenance Agent inside a home-intelligence system. Analyze maintenance "
    "records, appliance ages/condition, and home systems to find overdue or upcoming "
    "maintenance needs. Use priority 'urgent_attention' only for a genuine safety-relevant "
    "maintenance issue (e.g. very old water heater, no smoke alarms, reported leaks). Respond "
    "with JSON: {\"observations\": [string], \"recommendations\": [recommendation objects]}. Each "
    "recommendation object has: title, category ('maintenance'), room_id, room_name, priority, "
    "why_it_matters, recommended_action, expected_benefit, effort, estimated_cost "
    "{type,min,max,currency,is_estimate}, confidence, assumptions, "
    "requires_professional_assessment (true for anything electrical, gas, structural, or HVAC)."
)


def analyze(home: dict, maintenance_items: list[dict] | None = None) -> dict:
    appliances = [
        {
            "room_id": r.get("id"),
            "name": a.get("name"),
            "category": a.get("category"),
            "age_years": a.get("approximate_age_years"),
            "condition": a.get("condition"),
            "maintenance_status": a.get("maintenance_status"),
        }
        for r in (home.get("rooms") or [])
        for a in (r.get("appliances") or [])
    ]
    payload = {
        "appliances": appliances,
        "maintenance_items": maintenance_items or [],
        "security": home.get("security"),
    }
    result = run_agent("maintenance", SYSTEM_PROMPT, payload, ["observations", "recommendations"])
    result["recommendations"] = normalize_recommendations(
        result.get("recommendations", []), "maintenance", room_name_lookup(home)
    )
    return result
