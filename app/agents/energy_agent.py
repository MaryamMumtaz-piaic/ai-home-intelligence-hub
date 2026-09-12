from app.agents._shared import normalize_recommendations, room_name_lookup, run_agent

SYSTEM_PROMPT = (
    "You are the Energy Insight Agent inside a home-intelligence system. Analyze user-provided "
    "energy information, appliance usage, and cooling/heating habits to find potential energy "
    "opportunities. Never invent exact savings figures. Respond with JSON: "
    '{"observations": [string], "measurement_requirements": [string], "recommendations": '
    "[recommendation objects]}. Each recommendation object has: title, category ('energy'), "
    "room_id, room_name, priority, why_it_matters, recommended_action, expected_benefit "
    "(use hedged language like 'potential reduction' or 'estimated opportunity'), effort, "
    "estimated_cost {type,min,max,currency,is_estimate}, confidence, assumptions, "
    "requires_professional_assessment."
)


def analyze(home: dict) -> dict:
    appliances = [
        {
            "room_id": r.get("id"),
            "name": a.get("name"),
            "category": a.get("category"),
            "age_years": a.get("approximate_age_years"),
            "usage_frequency": a.get("usage_frequency"),
            "power_watts": a.get("estimated_power_watts"),
            "daily_hours": a.get("typical_daily_usage_hours"),
            "efficiency_label": a.get("energy_efficiency_label"),
        }
        for r in (home.get("rooms") or [])
        for a in (r.get("appliances") or [])
    ]
    payload = {
        "energy_profile": home.get("energy"),
        "appliances": appliances,
        "resident_count": home.get("resident_count"),
        "climate_zone_or_location": home.get("climate_zone_or_location"),
    }
    result = run_agent("energy", SYSTEM_PROMPT, payload, ["observations", "measurement_requirements", "recommendations"])
    result["recommendations"] = normalize_recommendations(
        result.get("recommendations", []), "energy", room_name_lookup(home)
    )
    return result
