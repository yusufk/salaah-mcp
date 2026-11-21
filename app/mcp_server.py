"""MCP server for the prayer time API, built on the official MCP Python SDK.

Each tool calls the same function as its REST endpoint, so both give the same answers.
The server speaks Streamable HTTP and is mounted into the FastAPI app at /mcp.
"""
import os

from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

from app.models.location_request import LocationRequest
from app.models.moon_visibility_request import MoonVisibilityRequest
from app.models.prayer_request import PrayerTimeRequest

mcp = MCPServer(
    name="Salaah MCP",
    instructions=(
        "Islamic prayer times, qiblah direction, sun and moon positions and crescent "
        "visibility for any latitude and longitude."
    ),
)


def _dump(result):
    if isinstance(result, list):
        return [item.model_dump(mode="json") for item in result]
    return result.model_dump(mode="json")


@mcp.tool(name="getPrayerTimes")
def get_prayer_times(request: PrayerTimeRequest) -> dict:
    """Prayer times (Fajr, sunrise, Zuhr, Asr, Maghrib, Isha, midnight) for a place and date."""
    from app.main import get_prayer_times as calc
    return _dump(calc(request))


@mcp.tool(name="getQiblahDirection")
def get_qiblah_direction(request: LocationRequest) -> dict:
    """Qiblah direction and distance to the Kaaba from a place."""
    from app.main import get_qiblah as calc
    return _dump(calc(request))


@mcp.tool(name="getSunInfo")
def get_sun_info(request: LocationRequest) -> dict:
    """Sunrise, solar noon, sunset and the sun's current position for a place."""
    from app.main import get_sun_info as calc
    return _dump(calc(request))


@mcp.tool(name="getMoonInfo")
def get_moon_info(request: LocationRequest) -> dict:
    """Moonrise, moonset, illumination and the moon's current position for a place."""
    from app.main import get_moon_info as calc
    return _dump(calc(request))


@mcp.tool(name="getMoonVisibility")
def get_moon_visibility(request: MoonVisibilityRequest) -> list:
    """Crescent visibility for the coming new moon, by the Yallop and Odeh criteria."""
    from app.main import get_moon_visibility as calc
    return _dump(calc(request))


def _transport_security():
    """Localhost only by default. Set SALAAH_ALLOWED_HOSTS (comma-separated) when deployed."""
    hosts = [h.strip() for h in os.environ.get("SALAAH_ALLOWED_HOSTS", "").split(",") if h.strip()]
    if not hosts:
        return None  # the SDK then allows only localhost
    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=hosts,
        allowed_origins=["https://" + h.split(":")[0] for h in hosts],
    )


def http_app():
    return mcp.streamable_http_app(streamable_http_path="/mcp", transport_security=_transport_security())
