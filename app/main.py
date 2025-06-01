from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from islamic_times.islamic_times import ITLocation
from pydantic import ValidationError
from app.models.prayer_request import PrayerTimeRequest
from app.models.prayer_response import PrayerTimeResponse
import logging
from datetime import datetime

# Initialize logging with more details
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.title = "Salaah MCP API"
app.description = "API for calculating Islamic prayer times using the Salaah MCP library."
mcp = FastApiMCP(app)

@app.post("/prayer_times", response_model=PrayerTimeResponse, operation_id="getPrayerTimes")
def get_prayer_times(request: PrayerTimeRequest):
    try:
        logger.info(f"Processing prayer time request for date: {request.date}")
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
        
        def validate_prayer_time(prayer_attr):
            value = getattr(prayers, prayer_attr, None)
            if hasattr(value, 'time'):
                return value.time
            return str(value) if value else None

        prayer_data = {
            'method': str(prayers.method),
            'fajr': validate_prayer_time('fajr'),
            'sunrise': validate_prayer_time('sunrise'),
            'zuhr': validate_prayer_time('zuhr'),
            'asr': validate_prayer_time('asr'),
            'sunset': validate_prayer_time('sunset'),
            'maghrib': validate_prayer_time('maghrib'),
            'isha': validate_prayer_time('isha'),
            'midnight': validate_prayer_time('midnight')
        }
        
        logger.debug(f"Converted prayer data: {prayer_data}")
        return PrayerTimeResponse(**prayer_data)
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating prayer times: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
# Mount the MCP server directly to your FastAPI app
mcp.mount()