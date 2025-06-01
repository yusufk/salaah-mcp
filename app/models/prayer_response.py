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
    fajr: Union[datetime, str]
    sunrise: Union[datetime, str]
    zuhr: Union[datetime, str]
    asr: Union[datetime, str]
    sunset: Union[datetime, str]
    maghrib: Union[datetime, str]
    isha: Union[datetime, str]
    midnight: Union[datetime, str]
