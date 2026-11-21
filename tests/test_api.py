"""Smoke tests for every endpoint, run in-process (no server needed)."""
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Johannesburg (the README example location)
JHB = {"latitude": -26.1528113, "longitude": 28.0049996}
DATE = "2026-11-21T00:00:00"


def test_root_redirects_to_docs():
    r = client.get("/", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "/docs"


@pytest.mark.parametrize("method", ["ISNA", "MWL", "Umm al-Qura", "Egyptian", "Karachi", "Tehran", "Jafari"])
def test_prayer_times_every_method(method):
    r = client.post("/prayer_times", json={**JHB, "date": DATE, "method": method})
    assert r.status_code == 200, r.text
    body = r.json()
    for key in ("fajr", "sunrise", "zuhr", "asr", "maghrib", "isha"):
        assert body[key], key
    # The method comes back as its readable name, not a Python repr.
    assert not body["method"].startswith("PrayerMethod(")


def test_prayer_times_are_in_order():
    r = client.post("/prayer_times", json={**JHB, "date": DATE, "method": "MWL"})
    body = r.json()
    times = [datetime.fromisoformat(str(body[k]).replace("Z", "+00:00"))
             for k in ("fajr", "sunrise", "zuhr", "asr", "maghrib", "isha")]
    assert times == sorted(times)


def test_prayer_times_rejects_unknown_method():
    r = client.post("/prayer_times", json={**JHB, "method": "EGYPTIAN"})
    assert r.status_code == 422


def test_qiblah_from_johannesburg_points_north_north_east():
    r = client.post("/qiblah", json=JHB)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["direction"] == "NNE"
    assert 10 < body["angle_decimal"] < 20
    assert 5000 < body["distance_km"] < 6000


@pytest.mark.parametrize("path", ["/sun", "/moon", "/moon/visibility"])
def test_celestial_endpoints(path):
    r = client.post(path, json={**JHB, "date": DATE})
    assert r.status_code == 200, r.text
    assert r.json()


def test_mcp_endpoint_is_mounted_without_sse():
    paths = {getattr(route, "path", "") for route in app.routes}
    assert "/mcp" in paths
    assert "/sse" not in paths


def test_mcp_http_lists_the_tools():
    headers = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}
    init = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "test", "version": "0"}}}
    with TestClient(app) as c:
        r = c.post("/mcp", json=init, headers=headers)
        assert r.status_code == 200, r.text
        sid = r.headers.get("mcp-session-id")
        h = {**headers, **({"mcp-session-id": sid} if sid else {})}
        c.post("/mcp", json={"jsonrpc": "2.0", "method": "notifications/initialized"}, headers=h)
        r = c.post("/mcp", json={"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, headers=h)
        assert r.status_code == 200, r.text
        for tool in ("getPrayerTimes", "getQiblahDirection", "getSunInfo", "getMoonInfo", "getMoonVisibility"):
            assert tool in r.text
