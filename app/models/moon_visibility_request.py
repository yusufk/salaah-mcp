from app.models.location_request import LocationRequest

class MoonVisibilityRequest(LocationRequest):
    days: int = 3
    criterion: int = 1
