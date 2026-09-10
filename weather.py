import requests

def get_current_weather(coords):
    # Unpack the latitude and longitude from the coordinates tuple
    lat, lon = coords
    url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "current" in data:
            current_data = data["current"]
            w_code = current_data["weather_code"]
            
            # Categorize the standard WMO weather codes with explicit values
            condition = "Sunny / Clear"
            if w_code in: 
                condition = "Partly Cloudy / Overcast"
            elif w_code in:
                condition = "Foggy / Smoggy"
            elif w_code >= 51: 
                condition = "Rain / Showers Imminent"
                
            return {
                "temp": current_data["temperature_2m"],
                "humidity": current_data["relative_humidity_2m"],
                "condition": condition
            }
    except Exception:
        pass
    return {"temp": "N/A", "humidity": "N/A", "condition": "Unavailable"}
import requests

def get_current_weather(coords):
    # Safely extract latitude and longitude from the passed coordinates tuple/list
    lat, lon = coords
    url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "current" in data:
            current_data = data["current"]
            w_code = current_data["weather_code"]
            
            # Categorize the standard World Meteorological Organization (WMO) codes
            condition = "Sunny / Clear"
            if w_code in: 
                condition = "Partly Cloudy / Overcast"
            elif w_code in:
                condition = "Foggy / Smoggy"
            elif w_code >= 51: 
                condition = "Rain / Showers Imminent"
                
            return {
                "temp": current_data["temperature_2m"],
                "humidity": current_data["relative_humidity_2m"],
                "condition": condition
            }
    except Exception:
        pass
    return {"temp": "N/A", "humidity": "N/A", "condition": "Unavailable"}
