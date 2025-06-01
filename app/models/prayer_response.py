from pydantic import BaseModel
from datetime import datetime

class PrayerTimeResponse(BaseModel):
    fajr: datetime
    sunrise: datetime
    dhuhr: datetime
    asr: datetime
    maghrib: datetime
    isha: datetime
    date: str
