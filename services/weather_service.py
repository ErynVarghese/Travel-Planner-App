# services/weather_service.py
import requests

def get_weather(destination, api_key):
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={destination}&appid={api_key}&units=metric'
    
    # Request weather data
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        data = response.json()
        weather = {
            "location": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "condition": data.get("weather", [])[0].get("description") if data.get("weather") else ""
        }
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        weather = {
            "location": destination,
            "temperature": "Error fetching temperature data",
            "condition": "Error fecthcing condition data"
        }
    
    return weather