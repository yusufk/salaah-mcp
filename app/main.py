from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from pyIslam.praytimes import PrayerConf, Prayer, LIST_FAJR_ISHA_METHODS
from app.models.prayer_request import PrayerTimeRequest
from app.models.prayer_response import PrayerTimeResponse
import logging

# Initialize logging with more details
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.title = "Salaah MCP API"
app.description = "API for calculating Islamic prayer times using the Salaah MCP library."

@app.post("/prayer_times", response_model=PrayerTimeResponse)
def get_prayer_times(request: PrayerTimeRequest):
    try:
        logger.info(f"Processing prayer time request for date: {request.date}")
        
        # Start with required fields
        conf_params = {
            "longitude": request.longitude,
            "latitude": request.latitude,
            "timezone": request.timezone
        }
        
        # Set method_index after configuring PrayerConf
        method_index = 0  # default to EGYPT_SURVEY
        
        # Add calculation method if specified
        if request.angle_ref is not None:
            angle_ref = request.angle_ref.to_int()
            conf_params["angle_ref"] = angle_ref
            method_index = angle_ref - 1  # Update method_index based on the actual method
            
        if request.asr_madhab is not None:
            conf_params["asr_madhab"] = request.asr_madhab.to_int()
            
        if request.enable_summer_time is not None:
            conf_params["enable_summer_time"] = request.enable_summer_time
        
        conf = PrayerConf(**conf_params)
        prayer = Prayer(conf, request.date)
        
        # Use the correct method_index for response
        times = {
            'method': LIST_FAJR_ISHA_METHODS[method_index].organizations[0],
            'fajr': str(prayer.fajr_time()),
            'sherook': str(prayer.sherook_time()),
            'dohr': str(prayer.dohr_time()),
            'asr': str(prayer.asr_time()),
            'maghreb': str(prayer.maghreb_time()),
            'ishaa': str(prayer.ishaa_time()),
            'midnight': str(prayer.midnight()),
            'qiyam': str(prayer.last_third_of_night())
        }
        
        logger.debug(f"Calculated prayer times: {times}")
        return PrayerTimeResponse(**times)
        
    except Exception as e:
        logger.error(f"Error calculating prayer times: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
# Mount the MCP server directly to your FastAPI app
mcp = FastApiMCP(app)
mcp.mount()