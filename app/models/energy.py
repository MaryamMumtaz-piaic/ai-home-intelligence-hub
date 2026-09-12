from typing import Optional, List
from pydantic import BaseModel, Field


class EnergyProfile(BaseModel):
    provider_or_tariff: Optional[str] = None
    approximate_monthly_bill: Optional[float] = Field(default=None, ge=0)
    currency: str = Field(default="USD", max_length=8)
    typical_monthly_consumption_kwh: Optional[float] = Field(default=None, ge=0)
    main_cooling_method: Optional[str] = None
    main_heating_method: Optional[str] = None
    lighting_type: Optional[str] = None
    solar_available: bool = False
    backup_power_available: bool = False
    peak_usage_periods: List[str] = Field(default_factory=list)
    frequently_used_appliances: List[str] = Field(default_factory=list)
    energy_concerns: Optional[str] = None
