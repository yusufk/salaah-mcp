from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Tuple

class CalculationMethod(str, Enum):
    MWL = "MWL"
    ISNA = "ISNA"
    EGYPT = "Egypt"
    MAKKAH = "Makkah"
    KARACHI = "Karachi"
    TEHRAN = "Tehran"
    JAFARI = "Jafari"

class AsrMethod(str, Enum):
    STANDARD = "Standard"
    HANAFI = "Hanafi"

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
    elevation: float = Field(
        default=0,
        description="Elevation in meters",
        ge=-420,
        le=8848
    )
    date: datetime = Field(
        default_factory=datetime.now,
        description="Date for prayer calculation"
    )
    method: CalculationMethod = Field(
        default=CalculationMethod.MWL,
        description="Prayer calculation method"
    )
    asr_method: AsrMethod = Field(
        default=AsrMethod.STANDARD,
        description="Asr calculation method"
    )
    timezone: float = Field(
        default=2.0,
        description="Timezone offset from UTC"
    )

    def get_coordinates(self) -> Tuple[float, float, float]:
        return (self.latitude, self.longitude, self.elevation)
    
    def get_date_tuple(self) -> Tuple[int, int, int]:
        return (self.date.year, self.date.month, self.date.day)