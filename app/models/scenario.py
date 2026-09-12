from typing import Optional, List
from pydantic import BaseModel, Field


class ScenarioRequest(BaseModel):
    home_id: str
    room_id: str
    scenario_type: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)


class ScenarioComparison(BaseModel):
    room_id: str
    scenario_type: str
    description: str
    current_state_summary: str
    proposed_change_summary: str
    potential_benefits: List[str] = Field(default_factory=list)
    possible_trade_offs: List[str] = Field(default_factory=list)
    estimated_effort: str
    affected_rooms: List[str] = Field(default_factory=list)
    required_follow_up_actions: List[str] = Field(default_factory=list)
    disclaimer: str = (
        "This is a planning simulation based on the information you provided, "
        "not an exact architectural or engineering simulation."
    )
