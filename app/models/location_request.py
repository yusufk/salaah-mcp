from pydantic import BaseModel
from datetime import datetime

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    elevation: float = 0
    temperature: float = 10
    pressure: float = 1010
    date: datetime = datetime.now()
