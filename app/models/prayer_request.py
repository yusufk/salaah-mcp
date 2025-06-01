from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class Method(str, Enum):
    KARACHI = "KARACHI"          # UISK (1)
    MUSLIM_LEAGUE = "MWL"        # Muslim World League (2)
    EGYPT_SURVEY = "EGYPT"       # Egyptian General Authority of Survey (3)
    UMM_ALQURA = "UMM_ALQURA"   # Umm al-Qura University, Makkah (4)
    ISNA = "ISNA"               # Islamic Society of North America (5)
    
    def to_int(self) -> int:
        return {
            "KARACHI": 1,        # University of Islamic Sciences, Karachi
            "MWL": 2,           # Muslim World League
            "EGYPT": 3,         # Egyptian General Authority of Survey
            "UMM_ALQURA": 4,    # Umm al-Qura University, Makkah
            "ISNA": 5           # Islamic Society of North America
        }[self.value]

class AsrMethod(str, Enum):
    STANDARD = "STANDARD"    # Shafii, Maliki, Hambali
    HANAFI = "HANAFI"       # Hanafi
    
    def to_int(self) -> int:
        return {"STANDARD": 1, "HANAFI": 2}[self.value]

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
    timezone: Optional[float] = Field(
        default=2.0,          # South Africa timezone
        description="Timezone offset from UTC"
    )
    angle_ref: Optional[Method] = Field(
        default=Method.KARACHI,
        alias="calculation_method",
        description="Prayer calculation method"
    )
    asr_madhab: Optional[AsrMethod] = Field(
        default=AsrMethod.HANAFI,
        alias="madhab",
        description="Madhab for Asr calculation (SHAFI or HANAFI)"
    )
    enable_summer_time: Optional[bool] = Field(
        default=False,
        description="Enable summer time adjustments"
    )
    date: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Date for prayer calculation"
    )