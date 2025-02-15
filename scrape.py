import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(lat, lon, unit_fix=True):
    """
    Fetches weather data for a given latitude and longitude using OpenWeatherMap API.

    Args:
        lat (str or float): Latitude
        lon (str or float): Longitude
        unit_fix (bool): True for metric (Celsius), False for imperial (Fahrenheit)

    Returns:
        dict: Weather data or error message
    """
    units = "metric" if unit_fix else "imperial"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "units": units,
    }

    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data.get("name", "Unknown"),
            "temperature": f"{data['main']['temp']}°{'C' if unit_fix else 'F'}",
            "humidity": f"{data['main']['humidity']}%",
            "weather": data["weather"][0]["description"],
            "wind_speed": f"{data['wind']['speed']} m/s",
            "precipitation": data.get("rain", {}).get("1h", 0),  # Rain in last 1 hour (default 0)
            "icon_url": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
        }
        return weather_info
    else:
        return {"error": f"Failed to fetch weather data. {response.json().get('message', 'Unknown error')}"}