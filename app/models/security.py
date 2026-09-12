from typing import Optional, List
from pydantic import BaseModel, Field


class SecurityProfile(BaseModel):
    entry_points: List[str] = Field(default_factory=list)
    door_locks_present: bool = True
    window_locks_present: bool = True
    outdoor_lighting: bool = False
    smoke_alarms: bool = False
    carbon_monoxide_alarms: bool = False
    emergency_exits_clear: bool = True
    first_aid_kit_available: bool = False
    fire_extinguisher_available: bool = False
    backup_communication_plan: bool = False
    important_emergency_notes: Optional[str] = Field(default=None, max_length=1000)
