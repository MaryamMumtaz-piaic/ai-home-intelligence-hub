from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.common import RoomType, NaturalLightLevel, HomeStyle, Priority
from app.models.furniture import FurnitureItem
from app.models.appliance import Appliance


class Room(BaseModel):
    id: Optional[str] = None
    home_id: str
    name: str = Field(min_length=1, max_length=100)
    room_type: RoomType
    length_m: float = Field(gt=0, le=100, description="Length in meters")
    width_m: float = Field(gt=0, le=100, description="Width in meters")
    ceiling_height_m: float = Field(default=2.7, gt=1.5, le=10)
    floor_level: int = Field(default=0, ge=-2, le=100)
    natural_light: NaturalLightLevel = NaturalLightLevel.MEDIUM
    window_count: int = Field(default=1, ge=0, le=50)
    door_count: int = Field(default=1, ge=0, le=20)
    primary_purpose: Optional[str] = Field(default=None, max_length=300)
    current_problems: List[str] = Field(default_factory=list)
    preferred_style: Optional[HomeStyle] = None
    priority: Priority = Priority.MEDIUM
    order: int = Field(default=0)
    furniture: List[FurnitureItem] = Field(default_factory=list)
    appliances: List[Appliance] = Field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @property
    def area_sqm(self) -> float:
        return round(self.length_m * self.width_m, 2)


class RoomCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    room_type: RoomType
    length_m: float = Field(gt=0, le=100)
    width_m: float = Field(gt=0, le=100)
    ceiling_height_m: float = Field(default=2.7, gt=1.5, le=10)
    floor_level: int = Field(default=0, ge=-2, le=100)
    natural_light: NaturalLightLevel = NaturalLightLevel.MEDIUM
    window_count: int = Field(default=1, ge=0, le=50)
    door_count: int = Field(default=1, ge=0, le=20)
    primary_purpose: Optional[str] = Field(default=None, max_length=300)
    current_problems: List[str] = Field(default_factory=list)
    preferred_style: Optional[HomeStyle] = None
    priority: Priority = Priority.MEDIUM


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    room_type: Optional[RoomType] = None
    length_m: Optional[float] = Field(default=None, gt=0, le=100)
    width_m: Optional[float] = Field(default=None, gt=0, le=100)
    ceiling_height_m: Optional[float] = Field(default=None, gt=1.5, le=10)
    floor_level: Optional[int] = Field(default=None, ge=-2, le=100)
    natural_light: Optional[NaturalLightLevel] = None
    window_count: Optional[int] = Field(default=None, ge=0, le=50)
    door_count: Optional[int] = Field(default=None, ge=0, le=20)
    primary_purpose: Optional[str] = Field(default=None, max_length=300)
    current_problems: Optional[List[str]] = None
    preferred_style: Optional[HomeStyle] = None
    priority: Optional[Priority] = None
    order: Optional[int] = None
