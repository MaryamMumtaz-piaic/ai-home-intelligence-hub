from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.common import HomeType, OwnershipStatus, HomeGoal
from app.models.room import Room
from app.models.lifestyle import LifestylePreferences
from app.models.energy import EnergyProfile
from app.models.security import SecurityProfile


class HomeProfile(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=1, max_length=100)
    home_type: HomeType
    climate_zone_or_location: Optional[str] = Field(default=None, max_length=150)
    resident_count: int = Field(default=1, ge=1, le=50)
    floor_count: int = Field(default=1, ge=1, le=50)
    approximate_total_area_sqm: Optional[float] = Field(default=None, gt=0, le=100000)
    ownership_status: OwnershipStatus = OwnershipStatus.OWNED
    main_goals: List[HomeGoal] = Field(default_factory=list)
    rooms: List[Room] = Field(default_factory=list)
    lifestyle: LifestylePreferences = Field(default_factory=LifestylePreferences)
    energy: EnergyProfile = Field(default_factory=EnergyProfile)
    security: SecurityProfile = Field(default_factory=SecurityProfile)
    setup_completed: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class HomeProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    home_type: HomeType
    climate_zone_or_location: Optional[str] = Field(default=None, max_length=150)
    resident_count: int = Field(default=1, ge=1, le=50)
    floor_count: int = Field(default=1, ge=1, le=50)
    approximate_total_area_sqm: Optional[float] = Field(default=None, gt=0, le=100000)
    ownership_status: OwnershipStatus = OwnershipStatus.OWNED
    main_goals: List[HomeGoal] = Field(default_factory=list)


class HomeProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    home_type: Optional[HomeType] = None
    climate_zone_or_location: Optional[str] = Field(default=None, max_length=150)
    resident_count: Optional[int] = Field(default=None, ge=1, le=50)
    floor_count: Optional[int] = Field(default=None, ge=1, le=50)
    approximate_total_area_sqm: Optional[float] = Field(default=None, gt=0, le=100000)
    ownership_status: Optional[OwnershipStatus] = None
    main_goals: Optional[List[HomeGoal]] = None
    lifestyle: Optional[LifestylePreferences] = None
    energy: Optional[EnergyProfile] = None
    security: Optional[SecurityProfile] = None
    setup_completed: Optional[bool] = None
