import logging

from pydantic import ValidationError

from app.models.recommendation import Recommendation
from app.services.json_store import read_collection, write_collection
from app.utils.dates import now_iso
from app.utils.ids import new_id

logger = logging.getLogger("ai_home_hub.recommendations")

COLLECTION = "recommendations"


def list_recommendations(
    home_id: str,
    category: str | None = None,
    room_id: str | None = None,
    priority: str | None = None,
    status: str | None = None,
) -> list[dict]:
    items = [r for r in read_collection(COLLECTION) if r.get("home_id") == home_id]
    if category:
        items = [r for r in items if r.get("category") == category]
    if room_id:
        items = [r for r in items if r.get("room_id") == room_id]
    if priority:
        items = [r for r in items if r.get("priority") == priority]
    if status:
        items = [r for r in items if r.get("status") == status]
    return items


def save_generated(home_id: str, recommendation_dicts: list[dict]) -> list[dict]:
    existing = read_collection(COLLECTION)
    existing_keys = {
        (r.get("home_id"), r.get("room_id"), r.get("title"))
        for r in existing
        if r.get("home_id") == home_id
    }
    now = now_iso()
    created = []
    for rec in recommendation_dicts:
        key = (home_id, rec.get("room_id"), rec.get("title"))
        if key in existing_keys:
            continue
        try:
            record = Recommendation(
                id=new_id("rec"),
                home_id=home_id,
                created_at=now,
                updated_at=now,
                **rec,
            ).model_dump()
        except ValidationError:
            # Defense in depth: agents should already sanitize their output via
            # normalize_recommendations, but a malformed record must never take down
            # the whole analysis request — skip it and keep the rest of the report.
            logger.warning("recommendations.save_generated.invalid_record_skipped")
            continue
        existing.append(record)
        existing_keys.add(key)
        created.append(record)
    write_collection(COLLECTION, existing)
    return created


def _update_status(recommendation_id: str, status: str) -> dict | None:
    items = read_collection(COLLECTION)
    for idx, rec in enumerate(items):
        if rec.get("id") == recommendation_id:
            rec["status"] = status
            rec["updated_at"] = now_iso()
            items[idx] = rec
            write_collection(COLLECTION, items)
            return rec
    return None


def save_recommendation(recommendation_id: str) -> dict | None:
    return _update_status(recommendation_id, "saved")


def complete_recommendation(recommendation_id: str) -> dict | None:
    return _update_status(recommendation_id, "completed")


def dismiss_recommendation(recommendation_id: str) -> dict | None:
    return _update_status(recommendation_id, "dismissed")
