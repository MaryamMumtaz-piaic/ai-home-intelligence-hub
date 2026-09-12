"""Improvement Planning Agent — sequences recommendations into a roadmap.

Deterministic Python: groups already-generated recommendations (from the other agents)
into quick wins / low-cost / medium-effort / larger projects and a suggested sequence,
based on their effort and cost fields.
"""


def build_plan(recommendations: list[dict]) -> dict:
    quick_wins, low_cost, medium_effort, larger_projects = [], [], [], []
    for rec in recommendations:
        effort = rec.get("effort", "medium")
        cost_type = (rec.get("estimated_cost") or {}).get("type", "none")
        title = rec.get("title", "Untitled")
        if effort == "low" and cost_type in ("none", "low"):
            quick_wins.append(title)
        elif cost_type in ("none", "low") and effort != "high":
            low_cost.append(title)
        elif effort == "medium" or cost_type == "medium":
            medium_effort.append(title)
        else:
            larger_projects.append(title)

    sequence = quick_wins + low_cost + medium_effort + larger_projects
    return {
        "quick_wins": quick_wins,
        "low_cost_improvements": low_cost,
        "medium_effort_improvements": medium_effort,
        "larger_projects": larger_projects,
        "suggested_sequence": sequence,
    }
