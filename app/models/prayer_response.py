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
    fajr: str
    sherook: str
    dohr: str
    asr: str
    maghreb: str
    ishaa: str
    midnight: str
    qiyam: str
