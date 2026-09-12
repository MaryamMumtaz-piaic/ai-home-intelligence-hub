from typing import Optional
from pydantic import BaseModel, Field

from app.models.common import FurnitureCategory, ConditionLevel, UsageFrequency, Priority


class FurniturePosition(BaseModel):
    x: float = Field(default=0, ge=0, description="Position from left as a percentage of room width (0-100)")
    y: float = Field(default=0, ge=0, description="Position from top as a percentage of room length (0-100)")


class FurnitureItem(BaseModel):
    id: Optional[str] = None
    room_id: str
    name: str = Field(min_length=1, max_length=100)
    category: FurnitureCategory
    width: float = Field(gt=0, le=2000, description="Width in cm")
    depth: float = Field(gt=0, le=2000, description="Depth in cm")
    height: Optional[float] = Field(default=None, gt=0, le=400, description="Height in cm")
    position: FurniturePosition = Field(default_factory=FurniturePosition)
    condition: ConditionLevel = ConditionLevel.GOOD
    usage_frequency: UsageFrequency = UsageFrequency.OFTEN
    importance: Priority = Priority.MEDIUM
    can_be_moved: bool = True
    blocks_movement: bool = False
    notes: Optional[str] = Field(default=None, max_length=500)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class FurnitureCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: FurnitureCategory
    width: float = Field(gt=0, le=2000)
    depth: float = Field(gt=0, le=2000)
    height: Optional[float] = Field(default=None, gt=0, le=400)
    position: FurniturePosition = Field(default_factory=FurniturePosition)
    condition: ConditionLevel = ConditionLevel.GOOD
    usage_frequency: UsageFrequency = UsageFrequency.OFTEN
    importance: Priority = Priority.MEDIUM
    can_be_moved: bool = True
    blocks_movement: bool = False
    notes: Optional[str] = Field(default=None, max_length=500)
