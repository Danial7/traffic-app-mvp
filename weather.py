import requests

def get_current_weather(coords):
    """Gathers live temperature, humidity, and clear/cloudy status states directly from coordinates."""
    url = f"https://open-meteo.com{coords[0]}&longitude={coords[1]}&current=temperature_2m,relative_humidity_2m,weather_code"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "current" in data:
            current_data = data["current"]
            w_code = current_data["weather_code"]
            
            # Basic map logic interpreting standard WMO Weather interpretation codes
            condition = "Sunny / Clear"
            if w_code in: condition = "Partly Cloudy / Overcast"
            elif w_code in: condition = "Foggy Conditions"
            elif w_code >= 51: condition = "Rain / Showers Imminent"
            
            return {
                "temp": current_data["temperature_2m"],
                "humidity": current_data["relative_humidity_2m"],
                "condition": condition
            }
    except Exception:
        pass
    return {"temp": "N/A", "humidity": "N/A", "condition": "Unavailable"}
