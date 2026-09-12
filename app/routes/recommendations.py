from fastapi import APIRouter

from app.models.recommendation import Recommendation
from app.services import recommendation_service
from app.utils.validation import not_found

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("", response_model=list[Recommendation])
def list_recommendations(
    home_id: str,
    category: str | None = None,
    room_id: str | None = None,
    priority: str | None = None,
    status: str | None = None,
):
    return recommendation_service.list_recommendations(home_id, category, room_id, priority, status)


@router.post("/{recommendation_id}/save", response_model=Recommendation)
def save_recommendation(recommendation_id: str):
    rec = recommendation_service.save_recommendation(recommendation_id)
    if rec is None:
        raise not_found("Recommendation", recommendation_id)
    return rec


@router.post("/{recommendation_id}/complete", response_model=Recommendation)
def complete_recommendation(recommendation_id: str):
    rec = recommendation_service.complete_recommendation(recommendation_id)
    if rec is None:
        raise not_found("Recommendation", recommendation_id)
    return rec


@router.post("/{recommendation_id}/dismiss", response_model=Recommendation)
def dismiss_recommendation(recommendation_id: str):
    rec = recommendation_service.dismiss_recommendation(recommendation_id)
    if rec is None:
        raise not_found("Recommendation", recommendation_id)
    return rec
