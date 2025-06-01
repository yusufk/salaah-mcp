from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from islamic_times.islamic_times import ITLocation
from pydantic import ValidationError
from app.models.prayer_request import PrayerTimeRequest
from app.models.prayer_response import PrayerTimeResponse
from app.models.location_request import LocationRequest
from app.models.qiblah_response import QiblahResponse
from app.models.celestial_response import SunResponse, MoonResponse, MoonVisibilityResponse
from app.models.moon_visibility_request import MoonVisibilityRequest
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
    

@app.post("/qiblah", response_model=QiblahResponse)
def get_qiblah(request: LocationRequest):
    try:
        location = ITLocation(
            latitude=request.latitude,
            longitude=request.longitude,
            elevation=request.elevation,
            temperature=request.temperature,
            pressure=request.pressure,
            date=request.date
        )
        mecca_info = location.mecca()
        # Parse the numeric distance value from the string
        distance_val = float(str(mecca_info.distance).split()[0].replace(',', ''))
        
        # Get the cardinal direction from the angle
        angle_str = str(mecca_info.angle)
        # Extract the decimal angle from the first part before tab
        angle_value = float(angle_str.split('\t')[0].replace('°', '').replace('+', ''))
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        idx = round(((angle_value + 360) % 360) / 22.5)
        cardinal_direction = directions[idx % 16]
        
        # Extract DMS format from the parentheses
        dms_format = angle_str.split('(')[1].strip(')')
        
        return QiblahResponse(
            distance_km=distance_val,
            distance_mi=distance_val / 1.60934,
            direction=cardinal_direction,
            angle_decimal=angle_value,
            angle_dms=dms_format
        )
    except Exception as e:
        logger.error(f"Error calculating qiblah: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sun", response_model=SunResponse)
def get_sun_info(request: LocationRequest):
    try:
        location = ITLocation(
            latitude=request.latitude,
            longitude=request.longitude,
            elevation=request.elevation,
            temperature=request.temperature,
            pressure=request.pressure,
            date=request.date
        )
        sun_info = location.sun()
        
        return SunResponse(
            sunrise=sun_info.sunrise,
            transit=sun_info.sun_transit,
            sunset=sun_info.sunset,
            apparent_altitude=float(sun_info.apparent_altitude.decimal),
            apparent_azimuth=float(sun_info.true_azimuth.decimal),
            distance_au=float(str(sun_info.geocentric_distance).split()[0]),
            apparent_declination=float(sun_info.apparent_declination.decimal),
            apparent_right_ascension=str(sun_info.apparent_right_ascension),
            greenwich_hour_angle=float(sun_info.greenwich_hour_angle.decimal),
            local_hour_angle=float(sun_info.local_hour_angle.decimal)
        )
    except Exception as e:
        logger.error(f"Error calculating sun info: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/moon", response_model=MoonResponse)
def get_moon_info(request: LocationRequest):
    try:
        location = ITLocation(
            latitude=request.latitude,
            longitude=request.longitude,
            elevation=request.elevation,
            temperature=request.temperature,
            pressure=request.pressure,
            date=request.date
        )
        moon_info = location.moon()
        logger.debug(f"Moon info attributes: {dir(moon_info)}")  # Debug available attributes
        
        return MoonResponse(
            moonrise=moon_info.moonrise,
            transit=moon_info.moon_transit,
            moonset=moon_info.moonset,
            illumination=float(moon_info.illumination),
            apparent_altitude=float(moon_info.apparent_altitude.decimal),
            azimuth=float(moon_info.true_azimuth.decimal),
            distance_km=float(str(moon_info.geocentric_distance).split()[0]),
            parallax=float(moon_info.parallax.decimal),
            topocentric_declination=float(moon_info.topocentric_declination.decimal),
            topocentric_right_ascension=str(moon_info.apparent_right_ascension),
            greenwich_hour_angle=float(moon_info.greenwich_hour_angle.decimal),
            local_hour_angle=float(moon_info.local_hour_angle.decimal)
        )
    except Exception as e:
        logger.error(f"Error calculating moon info: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/moon/visibility", response_model=list[MoonVisibilityResponse])
def get_moon_visibility(request: MoonVisibilityRequest):
    try:
        location = ITLocation(
            latitude=request.latitude,
            longitude=request.longitude,
            elevation=request.elevation,
            temperature=request.temperature,
            pressure=request.pressure,
            date=request.date
        )
        visibility_info = location.visibilities(days=request.days, criterion=request.criterion)
        
        # Create a response for each date's visibility data
        return [
            MoonVisibilityResponse(
                criterion=visibility_info.criterion,
                date=date,
                value=q_value,
                description=f"{class_desc}"
            )
            for date, q_value, class_desc in zip(
                visibility_info.dates,
                visibility_info.q_values,
                visibility_info.classifications
            )
        ]
    except Exception as e:
        logger.error(f"Error calculating moon visibility: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Mount the MCP server directly to your FastAPI app
mcp = FastApiMCP(app)
mcp.mount()