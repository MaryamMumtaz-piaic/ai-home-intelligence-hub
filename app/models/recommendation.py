from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.common import (
    RecommendationCategory,
    Priority,
    EffortLevel,
    ConfidenceLevel,
    RecommendationStatus,
    CostType,
)


class EstimatedCost(BaseModel):
    type: CostType = CostType.NONE
    min: float = Field(default=0, ge=0)
    max: float = Field(default=0, ge=0)
    currency: str = Field(default="USD", max_length=8)
    is_estimate: bool = True


class Recommendation(BaseModel):
    id: Optional[str] = None
    home_id: str
    title: str = Field(min_length=1, max_length=200)
    category: RecommendationCategory
    room_id: Optional[str] = None
    room_name: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    why_it_matters: str = Field(min_length=1, max_length=1000)
    recommended_action: str = Field(min_length=1, max_length=1000)
    expected_benefit: str = Field(min_length=1, max_length=500)
    effort: EffortLevel = EffortLevel.MEDIUM
    estimated_cost: EstimatedCost = Field(default_factory=EstimatedCost)
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    assumptions: List[str] = Field(default_factory=list)
    requires_professional_assessment: bool = False
    status: RecommendationStatus = RecommendationStatus.NEW
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class RecommendationList(BaseModel):
    recommendations: List[Recommendation] = Field(default_factory=list)
    generated_at: Optional[str] = None
    partial: bool = False
    failed_sections: List[str] = Field(default_factory=list)
