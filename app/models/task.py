from typing import Optional
from pydantic import BaseModel, Field

from app.models.common import Priority, TaskStatus, MaintenanceCategory


class HomeTask(BaseModel):
    id: Optional[str] = None
    home_id: str
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    category: MaintenanceCategory = MaintenanceCategory.OTHER
    room_id: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[str] = None
    estimated_cost: Optional[float] = Field(default=None, ge=0)
    estimated_effort: Optional[str] = None
    notes: Optional[str] = Field(default=None, max_length=500)
    source_recommendation_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class HomeTaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    category: MaintenanceCategory = MaintenanceCategory.OTHER
    room_id: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[str] = None
    estimated_cost: Optional[float] = Field(default=None, ge=0)
    estimated_effort: Optional[str] = None
    notes: Optional[str] = Field(default=None, max_length=500)
    source_recommendation_id: Optional[str] = None


class HomeTaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    category: Optional[MaintenanceCategory] = None
    room_id: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[str] = None
    estimated_cost: Optional[float] = Field(default=None, ge=0)
    estimated_effort: Optional[str] = None
    notes: Optional[str] = Field(default=None, max_length=500)
