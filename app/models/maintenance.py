from typing import Optional
from pydantic import BaseModel, Field

from app.models.common import MaintenanceCategory, MaintenanceStatus, Priority, ConditionLevel


class MaintenanceItem(BaseModel):
    id: Optional[str] = None
    home_id: str
    title: str = Field(min_length=1, max_length=150)
    category: MaintenanceCategory
    room_id: Optional[str] = None
    last_checked_date: Optional[str] = None
    next_suggested_date: Optional[str] = None
    condition: ConditionLevel = ConditionLevel.UNKNOWN
    priority: Priority = Priority.MEDIUM
    notes: Optional[str] = Field(default=None, max_length=500)
    status: MaintenanceStatus = MaintenanceStatus.NOT_STARTED
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class MaintenanceItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    category: MaintenanceCategory
    room_id: Optional[str] = None
    last_checked_date: Optional[str] = None
    next_suggested_date: Optional[str] = None
    condition: ConditionLevel = ConditionLevel.UNKNOWN
    priority: Priority = Priority.MEDIUM
    notes: Optional[str] = Field(default=None, max_length=500)
    status: MaintenanceStatus = MaintenanceStatus.NOT_STARTED
