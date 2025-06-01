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
            asr_type=request.asr_type.to_int() if request.asr_type else 0,
            find_local_tz=request.find_local_tz
        )

        # Configure the sunset angle after initialization if needed
        if request.sunset_angle != 0:
            location.sunset_angle = request.sunset_angle

        prayers = location.prayer_times()
        
        prayer_data = {
            'method': str(prayers.method),
            'fajr': prayers.fajr.time if hasattr(prayers.fajr, 'time') else str(prayers.fajr) if prayers.fajr else None,
            'sunrise': prayers.sunrise.time if hasattr(prayers.sunrise, 'time') else str(prayers.sunrise) if prayers.sunrise else None,
            'zuhr': prayers.zuhr.time if hasattr(prayers.zuhr, 'time') else str(prayers.zuhr) if prayers.zuhr else None,
            'asr': prayers.asr.time if hasattr(prayers.asr, 'time') else str(prayers.asr) if prayers.asr else None,
            'sunset': prayers.sunset.time if hasattr(prayers.sunset, 'time') else str(prayers.sunset) if prayers.sunset else None,
            'maghrib': prayers.maghrib.time if hasattr(prayers.maghrib, 'time') else str(prayers.maghrib) if prayers.maghrib else None,
            'isha': prayers.isha.time if hasattr(prayers.isha, 'time') else str(prayers.isha) if prayers.isha else None,
            'midnight': prayers.midnight.time if hasattr(prayers.midnight, 'time') else str(prayers.midnight) if prayers.midnight else None
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
mcp = FastApiMCP(app)
mcp.mount()