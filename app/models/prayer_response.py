from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Union

class MoonVisibilityData(BaseModel):
    datetime: datetime
    value: float
    description: str

class MoonVisibility(BaseModel):
    criterion: str
    observations: List[MoonVisibilityData]

class PrayerTimeResponse(BaseModel):
    method: str
    imsak: str
    fajr: str
    sunrise: str
    dhuhr: str
    asr: str
    sunset: str
    maghrib: str
    isha: str
    midnight: str
