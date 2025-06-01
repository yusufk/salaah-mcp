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

class AsrMethodType(str, Enum):
    SHAFI = "SHAFI"      # Standard method for Shafi'i, Maliki, and Hanbali schools
    HANAFI = "HANAFI"    # Method for Hanafi school

    def to_int(self) -> int:
        return 1 if self == AsrMethodType.HANAFI else 0

class PrayerTimeRequest(BaseModel):
    latitude: float = Field(
        default=-26.1528113,  # Johannesburg
        description="Latitude of location",
        ge=-90,
        le=90
    )
    longitude: float = Field(
        default=28.0049996,   # Johannesburg
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
    asr_type: Optional[AsrMethodType] = Field(
        default=AsrMethodType.SHAFI,
        description="Asr calculation method (SHAFI for Shafi'i/Maliki/Hanbali, HANAFI for Hanafi school)"
    )
    find_local_tz: Optional[bool] = Field(
        default=True,
        description="Auto-detect timezone"
    )