"""Critic and Validation Agent.

Runs as deterministic Python rather than a second model call: this step needs to be
reliable and reproducible (dedupe/contradiction-checking benefits from determinism far
more than from additional model creativity), and it keeps the pipeline resilient even
when every AI sub-agent has failed.
"""

_TITLE_STOPWORDS = {"the", "a", "an", "your", "for", "in", "of", "to"}


def _title_key(title: str) -> str:
    words = [w for w in title.lower().split() if w not in _TITLE_STOPWORDS]
    return " ".join(sorted(words))


def review(recommendations: list[dict]) -> list[dict]:
    """Deduplicates near-identical recommendations (same normalized title + room),
    drops recommendations missing required fields, and caps unrealistic claims."""
    seen: dict[tuple[str, str], dict] = {}
    for rec in recommendations:
        if not isinstance(rec, dict):
            continue
        if not rec.get("title") or not rec.get("recommended_action"):
            continue
        key = (_title_key(rec["title"]), rec.get("room_id") or "")
        if key in seen:
            existing = seen[key]
            priority_rank = {"urgent_attention": 3, "high": 2, "medium": 1, "low": 0}
            if priority_rank.get(rec.get("priority"), 0) > priority_rank.get(existing.get("priority"), 0):
                seen[key] = rec
            continue
        seen[key] = rec

    cleaned = list(seen.values())
    for rec in cleaned:
        cost = rec.get("estimated_cost") or {}
        cost["is_estimate"] = True
        rec["estimated_cost"] = cost
        if rec.get("priority") == "urgent_attention" and rec.get("category") not in ("safety", "maintenance"):
            rec["priority"] = "high"
    return cleaned
