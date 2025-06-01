# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
from datetime import datetime
from islamic_times.islamic_times import ITLocation
from islamic_times.dataclasses import PrayerTimes, Visibilities

initialize_app()


@https_fn.on_request()
def on_get_prayertime(req: https_fn.Request) -> https_fn.Response:
    location: ITLocation = ITLocation(
    latitude=req.args.get('latitude', -26.1528113),
    longitude=req.args.get('longitude', 28.0049996),
    elevation=req.args.get('elevation', 1753),
    temperature=req.args.get('temperature', 20),
    pressure=req.args.get('pressure', 102),
    date=req.args.get('date',datetime.now),
    method='Egyptian',
    asr_type=req.args.get('asr_type', 0),
	find_local_tz=True
    )

    # Calculate prayer times and return them
    prayers: PrayerTimes = location.prayer_times()
    return https_fn.Response(prayers.to_json(), mimetype='application/json', status=200)
