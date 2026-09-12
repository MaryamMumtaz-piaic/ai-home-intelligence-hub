from typing import Optional
from pydantic import BaseModel, Field

from app.models.common import ApplianceCategory, ConditionLevel, UsageFrequency, MaintenanceStatus


class Appliance(BaseModel):
    id: Optional[str] = None
    room_id: str
    name: str = Field(min_length=1, max_length=100)
    category: ApplianceCategory
    approximate_age_years: Optional[float] = Field(default=None, ge=0, le=100)
    usage_frequency: UsageFrequency = UsageFrequency.OFTEN
    estimated_power_watts: Optional[float] = Field(default=None, ge=0, le=20000)
    typical_daily_usage_hours: Optional[float] = Field(default=None, ge=0, le=24)
    condition: ConditionLevel = ConditionLevel.GOOD
    maintenance_status: MaintenanceStatus = MaintenanceStatus.NOT_STARTED
    energy_efficiency_label: Optional[str] = Field(default=None, max_length=20)
    notes: Optional[str] = Field(default=None, max_length=500)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ApplianceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: ApplianceCategory
    approximate_age_years: Optional[float] = Field(default=None, ge=0, le=100)
    usage_frequency: UsageFrequency = UsageFrequency.OFTEN
    estimated_power_watts: Optional[float] = Field(default=None, ge=0, le=20000)
    typical_daily_usage_hours: Optional[float] = Field(default=None, ge=0, le=24)
    condition: ConditionLevel = ConditionLevel.GOOD
    maintenance_status: MaintenanceStatus = MaintenanceStatus.NOT_STARTED
    energy_efficiency_label: Optional[str] = Field(default=None, max_length=20)
    notes: Optional[str] = Field(default=None, max_length=500)
