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
    latitude: float = Field(
        default=-26.1528113,
        description="Latitude of location",
        ge=-90,
        le=90
    )
    longitude: float = Field(
        default=28.0049996,
        description="Longitude of location",
        ge=-180,
        le=180
    )
    elevation: int = Field(
        default=1753,
        description="Elevation in meters",
        ge=-420,  # Dead Sea is lowest point on Earth
        le=8848   # Mount Everest height
    )
    temperature: int = Field(
        default=20,
        description="Temperature in celsius",
        ge=-89,  # Lowest recorded temperature
        le=57    # Highest recorded temperature
    )
    pressure: int = Field(
        default=102,
        description="Atmospheric pressure in kPa",
        ge=87,   # Minimum reasonable pressure
        le=108   # Maximum reasonable pressure
    )
    date: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Date for prayer calculation (defaults to noon today)"
    )
    method: CalculationMethod = Field(
        default=CalculationMethod.EGYPTIAN,
        description="Prayer time calculation method"
    )
    asr_type: int = Field(
        default=0,
        description="Asr calculation type",
        ge=0,
        le=1
    )
    find_local_tz: bool = Field(
        default=True,
        description="Auto-detect timezone"
    )