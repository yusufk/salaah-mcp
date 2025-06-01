from pydantic import BaseModel

class QiblahResponse(BaseModel):
    distance_km: float
    distance_mi: float
    direction: str
    angle_decimal: float
    angle_dms: str
