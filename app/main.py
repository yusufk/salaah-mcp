from fastapi import FastAPI
from islamic_times.islamic_times import ITLocation
from app.models.prayer_request import PrayerTimeRequest
from app.models.prayer_response import PrayerTimeResponse
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/prayer_times", response_model=PrayerTimeResponse)
def get_prayer_times(request: PrayerTimeRequest):
    location = ITLocation(
        latitude=request.latitude,
        longitude=request.longitude,
        elevation=request.elevation,
        temperature=request.temperature,
        pressure=request.pressure,
        date=request.date,
        method=request.method,
        asr_type=request.asr_type,
        find_local_tz=request.find_local_tz
    )

    prayers = location.prayer_times()
    logging.info(f"Prayer times for {request.date} at {request.latitude}, {request.longitude}: {prayers}")
    
    return PrayerTimeResponse(**prayers.to_json())