import requests
import polyline

def get_coordinates(location_name):
    """Converts a textual city/area name into precise coordinates using Nominatim."""
    url = f"https://openstreetmap.org{location_name},+Karachi,+Pakistan&format=json&limit=1"
    headers = {"User-Agent": "KarachiTrafficMVPApp/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None

def get_route_and_eta(start_coords, end_coords):
    """Fetches the optimal driving route geometry and base duration via OSRM."""
    url = f"http://project-osrm.org{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=full&geometries=polyline"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data and "routes" in data and len(data["routes"]) > 0:
            route = data["routes"][0]
            # OSRM returns base duration in seconds; convert to minutes
            duration_mins = round(route["duration"] / 60)
            geometry = route["geometry"]
            # Decode the geometry string into a list of lat/lng coordinate pairs
            decoded_points = polyline.decode(geometry)
            return {"duration_mins": duration_mins, "path_points": decoded_points}
    except Exception:
        pass
    return None

def fetch_route_hazards(start_coords, ors_key):
    """Queries OpenRouteService for active safety incidents and road barriers."""
    # Bounding box coordinates generated roughly around the starting focal point for MVP scale
    url = f"https://openrouteservice.org{start_coords[1]-0.1},{start_coords[0]-0.1},{start_coords[1]+0.1},{start_coords[0]+0.1}"
    headers = {"Authorization": ors_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Extract distinct human-readable details about current blockades or hazard warnings
            incidents = [feature["properties"]["description"] for feature in data.get("features", []) if "description" in feature["properties"]]
            return incidents if incidents else ["No critical road incident barriers reported directly via global geo-feeds."]
    except Exception:
        pass
    return ["Unable to pull localized incident layers at this exact moment."]
