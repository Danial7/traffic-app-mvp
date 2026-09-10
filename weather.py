import requests

def get_current_weather(coords):
    lat, lon = coords
    url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "current" in data:
            current_data = data["current"]
            w_code = current_data["weather_code"]
            
            # Categorize the standard WMO weather code into readable text
            condition = "Sunny / Clear"
            if w_code in: 
                condition = "Partly Cloudy / Overcast"
            elif w_code in: 
                condition = "Rain / Showers Imminent"
            elif w_code >= 71: 
                condition = "Severe Weather Conditions"
                
            return {
                "temp": current_data["temperature_2m"],
                "humidity": current_data["relative_humidity_2m"],
                "condition": condition
            }
    except Exception:
        pass
    return {"temp": "N/A", "humidity": "N/A", "condition": "Unavailable"}
