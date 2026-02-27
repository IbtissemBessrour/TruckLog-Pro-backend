import requests
from django.conf import settings

def geocode_location(location_name):
    """Convert text location → coordinates [lng, lat]"""
    url = "https://api.openrouteservice.org/geocode/search"
    params = {"api_key": settings.ORS_API_KEY, "text": location_name, "size": 1}
    response = requests.get(url, params=params)
    data = response.json()
    if "features" in data and len(data["features"]) > 0:
        return data["features"][0]["geometry"]["coordinates"]
    return None

def get_route(coordinates_list):
    """Get route distance/duration/polyline"""
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": settings.ORS_API_KEY, "Content-Type": "application/json"}
    body = {"coordinates": coordinates_list}
    response = requests.post(url, json=body, headers=headers)
    data = response.json()
    if "routes" in data:
        route = data["routes"][0]
        summary = route["summary"]
        return {
            "distance_miles": summary["distance"] * 0.000621371,
            "duration_hours": summary["duration"] / 3600,
            "polyline": route["geometry"]
        }
    return None