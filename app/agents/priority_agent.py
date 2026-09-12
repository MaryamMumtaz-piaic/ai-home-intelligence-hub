"""Cost and Priority Agent — organizes recommendations by impact/effort/cost/urgency.

Deterministic Python rather than a model call, so ordering is stable and explainable.
"""

_PRIORITY_WEIGHT = {"urgent_attention": 4, "high": 3, "medium": 2, "low": 1}
_EFFORT_WEIGHT = {"low": 3, "medium": 2, "high": 1}
_COST_WEIGHT = {"none": 3, "low": 2, "medium": 1, "high": 0}


def _score(rec: dict) -> float:
    priority = _PRIORITY_WEIGHT.get(rec.get("priority"), 2)
    effort = _EFFORT_WEIGHT.get(rec.get("effort"), 2)
    cost = _COST_WEIGHT.get((rec.get("estimated_cost") or {}).get("type"), 2)
    return priority * 10 + effort * 2 + cost


def prioritize(recommendations: list[dict]) -> list[dict]:
    return sorted(recommendations, key=_score, reverse=True)


def quick_wins(recommendations: list[dict], limit: int = 5) -> list[str]:
    wins = [
        r for r in recommendations
        if r.get("effort") == "low" and (r.get("estimated_cost") or {}).get("type") in ("none", "low")
    ]
    return [r["title"] for r in wins[:limit]]


def top_actions(recommendations: list[dict], limit: int = 3) -> list[str]:
    return [r["title"] for r in prioritize(recommendations)[:limit]]


def high_priority_issues(recommendations: list[dict]) -> list[str]:
    return [r["title"] for r in recommendations if r.get("priority") in ("high", "urgent_attention")]
