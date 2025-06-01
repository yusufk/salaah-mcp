from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class SunResponse(BaseModel):
    sunrise: datetime
    transit: datetime
    sunset: datetime
    apparent_altitude: float
    apparent_azimuth: float
    distance_au: float
    apparent_declination: float
    apparent_right_ascension: str
    greenwich_hour_angle: float
    local_hour_angle: float

class MoonResponse(BaseModel):
    moonrise: datetime
    transit: datetime
    moonset: datetime
    illumination: float
    apparent_altitude: float
    azimuth: float
    distance_km: float
    parallax: float
    topocentric_declination: float
    topocentric_right_ascension: str
    greenwich_hour_angle: float
    local_hour_angle: float

class MoonPhase(BaseModel):
    phase: str
    date: datetime

class MoonVisibilityResponse(BaseModel):
    criterion: str
    date: datetime
    value: float
    description: str
