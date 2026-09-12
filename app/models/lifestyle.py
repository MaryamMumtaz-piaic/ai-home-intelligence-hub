from typing import Optional
from pydantic import BaseModel

from app.models.common import HomeStyle


class LifestylePreferences(BaseModel):
    works_from_home: bool = False
    hosts_guests_often: bool = False
    has_children: bool = False
    has_pets: bool = False
    prefers_open_spaces: bool = True
    prefers_decorative_interiors: bool = False
    top_priority: Optional[str] = None
    has_accessibility_considerations: bool = False
    accessibility_notes: Optional[str] = None
    prefers_low_cost_changes: bool = True
    weekly_maintenance_time_hours: Optional[float] = None
    preferred_style: HomeStyle = HomeStyle.UNDECIDED
