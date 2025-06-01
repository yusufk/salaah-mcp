from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from app.tools.praytimes import PrayTimes
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

@app.post("/prayer_times", response_model=PrayerTimeResponse, operation_id="getPrayerTimes")
def get_prayer_times(request: PrayerTimeRequest):
    try:
        logger.info(f"Processing prayer time request for date: {request.date}")
        
        # Initialize PrayTimes with the requested method
        prayer_calc = PrayTimes(request.method.value)
        
        # Set Asr calculation method
        prayer_calc.adjust({'asr': request.asr_method.value})
        
        # Calculate prayer times
        times = prayer_calc.getTimes(
            request.get_date_tuple(),
            request.get_coordinates(),
            request.timezone
        )
        
        logger.debug(f"Calculated prayer times: {times}")
        
        # Create response with method and times
        response_data = {
            'method': prayer_calc.getMethod(),
            **times  # Prayer times are already using correct keys
        }
        
        return PrayerTimeResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error calculating prayer times: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
# Mount the MCP server directly to your FastAPI app
mcp = FastApiMCP(app)
mcp.mount()