from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class CalculationMethod(str, Enum):
    ISNA = "ISNA"
    MWL = "MWL"
    UMM_AL_QURA = "Umm al-Qura"
    EGYPTIAN = "Egyptian"
    KARACHI = "Karachi"
    TEHRAN = "Tehran"
    JAFARI = "Jafari"

class PrayerTimeRequest(BaseModel):
    # Required fields
    latitude: float = Field(
        description="Latitude of location",
        ge=-90,
        le=90
    )
    longitude: float = Field(
        description="Longitude of location",
        ge=-180,
        le=180
    )
    
    # Optional fields with defaults
    elevation: Optional[int] = Field(
        default=1753,
        description="Elevation in meters",
        ge=-420,  # Dead Sea is lowest point on Earth
        le=8848   # Mount Everest height
    )
    temperature: Optional[int] = Field(
        default=20,
        description="Temperature in celsius",
        ge=-89,  # Lowest recorded temperature
        le=57    # Highest recorded temperature
    )
    pressure: Optional[int] = Field(
        default=102,
        description="Atmospheric pressure in kPa",
        ge=87,   # Minimum reasonable pressure
        le=108   # Maximum reasonable pressure
    )
    date: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Date for prayer calculation (defaults to current time)"
    )
    method: Optional[CalculationMethod] = Field(
        default=CalculationMethod.KARACHI,
        description="Prayer time calculation method"
    )
    asr_type: Optional[int] = Field(
        default=0,
        description="Asr calculation type",
        ge=0,
        le=1
    )
    find_local_tz: Optional[bool] = Field(
        default=True,
        description="Auto-detect timezone"
    )