# Salaah MCP (Muslim Community Prayer Times)

A FastAPI and MCP service providing Islamic prayer times calculations using the [PrayTimes.org](http://praytimes.org/) library.

## Acknowledgments

Prayer time calculations are powered by [PrayTimes.org](http://praytimes.org/)
- Copyright (C) 2007-2011 PrayTimes.org
- Licensed under GNU LGPL v3.0
- Original work by Hamid Zarrabi-Zadeh

## Dependencies

This project relies on the following main dependencies:
- FastAPI: Web framework for building APIs
- FastAPI MCP: Muslim Community Platform integration
- Pydantic: Data validation

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install fastapi uvicorn
pip install git+https://github.com/tadata-org/fastapi_mcp.git
```

## Usage

Run the server:
```bash
python run.py
```

Or with uvicorn directly:
```bash
uvicorn app.main:app --reload
```

## API

### Calculate Prayer Times

`POST /prayer_times`

Example request:
```json
{
  "latitude": -26.1528113,
  "longitude": 28.0049996,
  "method": "EGYPTIAN"
}
```

Example response:
```json
{
  "method": "Egyptian General Authority of Survey (Egypt)",
  "fajr": "2025-06-01T05:19:11.373053+02:00",
  "sunrise": "2025-06-01T06:47:44.369263+02:00",
  "zuhr": "2025-06-01T12:05:43.358460+02:00",
  "asr": "2025-06-01T15:23:52.560113+02:00",
  "sunset": "2025-06-01T17:23:52.560113+02:00",
  "maghrib": "2025-06-01T17:23:52.560113+02:00",
  "isha": "2025-06-01T18:43:09.341111+02:00",
  "midnight": "2025-06-02T00:06:02.228763+02:00"
}
```

## Available Calculation Methods

- ISNA: Islamic Society of North America
- MWL: Muslim World League
- UMM_AL_QURA: Umm al-Qura University, Makkah
- EGYPTIAN: Egyptian General Authority of Survey
- KARACHI: University of Islamic Sciences, Karachi
- TEHRAN: Institute of Geophysics, University of Tehran
- JAFARI: Shia Ithna Ashari, Leva Research Institute, Qom
