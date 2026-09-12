from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class HomeAnalysisRequest(BaseModel):
    home_id: str


class RoomAnalysisRequest(BaseModel):
    home_id: str
    room_id: str


class IntelligenceCategoryScore(BaseModel):
    category: str
    score: int = Field(ge=0, le=100)
    label: str
    summary: str


class AgentSectionResult(BaseModel):
    agent: str
    succeeded: bool = True
    error: Optional[str] = None
    summary: Optional[str] = None


class HomeIntelligenceReport(BaseModel):
    home_id: str
    home_name: str
    room_count: int
    furniture_count: int
    appliance_count: int
    open_task_count: int
    analysis_date: str
    data_completeness_percent: int = Field(ge=0, le=100)
    category_scores: List[IntelligenceCategoryScore] = Field(default_factory=list)
    top_actions: List[str] = Field(default_factory=list)
    quick_wins: List[str] = Field(default_factory=list)
    high_priority_issues: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    suggested_next_step: Optional[str] = None
    room_summaries: List[Dict] = Field(default_factory=list)
    agent_sections: List[AgentSectionResult] = Field(default_factory=list)
    partial: bool = False
