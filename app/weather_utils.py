import requests


def get_weather_data(latitude, longitude, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial"  # Use 'metric' for Celsius
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract relevant data from the API response
        weather_info = {
            "main_condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"]["deg"],
            "cloud_cover": data["clouds"]["all"],
            "rain": data.get("rain", {}).get("1h", 0),  # Precipitation in the last hour
            "sunset": data["sys"]["sunset"],
            "geo": {
                "city": data["name"],
                "country": data["sys"]["country"],
                "coordinates": {
                    "lat": data["coord"]["lat"],
                    "lon": data["coord"]["lon"]
                }
            }
        }
        return weather_info
    else:
        return None  # Handle error if API fails
