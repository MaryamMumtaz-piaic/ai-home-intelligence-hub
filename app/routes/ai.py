from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from app.agents import orchestrator
from app.models.analysis import HomeAnalysisRequest, HomeIntelligenceReport, RoomAnalysisRequest
from app.models.recommendation import RecommendationList
from app.models.scenario import ScenarioComparison, ScenarioRequest
from app.services import home_service, maintenance_service, recommendation_service, task_service
from app.utils.helpers import count_appliances, count_furniture
from app.utils.validation import not_found

router = APIRouter(prefix="/api/ai", tags=["ai"])

ANALYSIS_FAILURE_MESSAGE = (
    "We couldn't complete your home analysis right now. "
    "Your saved home information is still available. Please try again."
)


class CategoryRequest(BaseModel):
    home_id: str
    category: str | None = None
    room_id: str | None = None


class HomeIdBody(BaseModel):
    home_id: str


def _require_home(home_id: str) -> dict:
    home = home_service.get_home(home_id)
    if home is None:
        raise not_found("Home", home_id)
    return home


@router.post("/analyze-home", response_model=HomeIntelligenceReport)
async def analyze_home(body: HomeAnalysisRequest):
    home = _require_home(body.home_id)
    try:
        result = await run_in_threadpool(orchestrator.analyze_home, home)
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=ANALYSIS_FAILURE_MESSAGE)

    created = recommendation_service.save_generated(body.home_id, result.get("recommendations", []))
    open_tasks = [t for t in task_service.list_tasks(body.home_id) if t.get("status") not in ("completed", "archived")]

    report = HomeIntelligenceReport(
        home_id=body.home_id,
        home_name=home.get("name", ""),
        room_count=len(home.get("rooms") or []),
        furniture_count=count_furniture(home),
        appliance_count=count_appliances(home),
        open_task_count=len(open_tasks),
        analysis_date=datetime.now(timezone.utc).isoformat(),
        data_completeness_percent=result.get("data_completeness_percent", 0),
        category_scores=result.get("category_scores", []),
        top_actions=result.get("top_actions", []),
        quick_wins=result.get("quick_wins", []),
        high_priority_issues=result.get("high_priority_issues", []),
        missing_information=result.get("missing_information", []),
        suggested_next_step=result.get("suggested_next_step"),
        room_summaries=result.get("room_summaries", []),
        agent_sections=result.get("agent_sections", []),
        partial=result.get("partial", False),
    )
    return report


@router.post("/analyze-room")
async def analyze_room(body: RoomAnalysisRequest):
    home = _require_home(body.home_id)
    room = next((r for r in (home.get("rooms") or []) if r.get("id") == body.room_id), None)
    if room is None:
        raise not_found("Room", body.room_id)
    try:
        result = await run_in_threadpool(orchestrator.analyze_room, home, body.room_id)
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=ANALYSIS_FAILURE_MESSAGE)

    if result.get("recommendations"):
        recommendation_service.save_generated(body.home_id, result["recommendations"])
    return result


@router.post("/generate-recommendations", response_model=RecommendationList)
async def generate_recommendations(body: CategoryRequest):
    home = _require_home(body.home_id)
    try:
        recs = await run_in_threadpool(orchestrator.generate_recommendations, home, body.category, body.room_id)
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=ANALYSIS_FAILURE_MESSAGE)
    created = recommendation_service.save_generated(body.home_id, recs)
    return RecommendationList(recommendations=created, generated_at=datetime.now(timezone.utc).isoformat())


@router.post("/compare-scenario", response_model=ScenarioComparison)
async def compare_scenario(body: ScenarioRequest):
    home = _require_home(body.home_id)
    room = next((r for r in (home.get("rooms") or []) if r.get("id") == body.room_id), None)
    if room is None:
        raise not_found("Room", body.room_id)
    try:
        result = await run_in_threadpool(
            orchestrator.compare_scenario, home, body.room_id, body.scenario_type, body.description
        )
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=ANALYSIS_FAILURE_MESSAGE)

    return ScenarioComparison(
        room_id=body.room_id,
        scenario_type=body.scenario_type,
        description=body.description,
        current_state_summary=result.get("current_state_summary", ""),
        proposed_change_summary=result.get("proposed_change_summary", body.description),
        potential_benefits=result.get("potential_benefits", []),
        possible_trade_offs=result.get("possible_trade_offs", []),
        estimated_effort=result.get("estimated_effort", "unknown"),
        affected_rooms=result.get("affected_rooms", []),
        required_follow_up_actions=result.get("required_follow_up_actions", []),
    )


@router.post("/energy-insights", response_model=RecommendationList)
async def energy_insights(body: HomeIdBody):
    home = _require_home(body.home_id)
    try:
        recs = await run_in_threadpool(orchestrator.energy_insights, home)
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=ANALYSIS_FAILURE_MESSAGE)
    created = recommendation_service.save_generated(body.home_id, recs)
    return RecommendationList(recommendations=created, generated_at=datetime.now(timezone.utc).isoformat())


@router.post("/maintenance-plan", response_model=RecommendationList)
async def maintenance_plan(body: HomeIdBody):
    home = _require_home(body.home_id)
    items = maintenance_service.list_items(body.home_id)
    try:
        recs = await run_in_threadpool(orchestrator.maintenance_plan, home, items)
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=ANALYSIS_FAILURE_MESSAGE)
    created = recommendation_service.save_generated(body.home_id, recs)
    return RecommendationList(recommendations=created, generated_at=datetime.now(timezone.utc).isoformat())


@router.post("/organization-plan", response_model=RecommendationList)
async def organization_plan(body: HomeIdBody):
    home = _require_home(body.home_id)
    try:
        recs = await run_in_threadpool(orchestrator.organization_plan, home)
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=ANALYSIS_FAILURE_MESSAGE)
    created = recommendation_service.save_generated(body.home_id, recs)
    return RecommendationList(recommendations=created, generated_at=datetime.now(timezone.utc).isoformat())
