from app.agents._shared import normalize_recommendations, room_name_lookup, run_agent

SYSTEM_PROMPT = (
    "You are the Safety Awareness Agent inside a home-intelligence system. Provide only general "
    "home-safety awareness guidance based on entry points, alarms, exits, and lighting the user "
    "reported. You are not a professional security assessor or emergency service — never claim "
    "to guarantee security. Respond with JSON: {\"observations\": [string], \"missing_information\": "
    '[string], "recommendations": [recommendation objects]}. Each recommendation object has: '
    "title, category ('safety'), room_id, room_name, priority (use 'urgent_attention' for missing "
    "smoke alarms or blocked emergency exits), why_it_matters, recommended_action, "
    "expected_benefit, effort, estimated_cost {type,min,max,currency,is_estimate}, confidence, "
    "assumptions, requires_professional_assessment."
)


def analyze(home: dict) -> dict:
    payload = {"security": home.get("security"), "resident_count": home.get("resident_count")}
    result = run_agent("safety", SYSTEM_PROMPT, payload, ["observations", "missing_information", "recommendations"])
    result["recommendations"] = normalize_recommendations(
        result.get("recommendations", []), "safety", room_name_lookup(home)
    )
    return result
