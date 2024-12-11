from flask import Blueprint, render_template
from app.weather_utils import get_weather_data  # Import the function to fetch current weather data

game_viewer = Blueprint('game_viewer', __name__)


@game_viewer.route('/game_viewer')
def show_game_viewer():
    # Coordinates for Truist Park, Georgia
    latitude = 33.8915
    longitude = -84.4675
    api_key = "59bdf5e30c855e10368f12c17e6b8e0b"

    # Fetch current weather data for Truist Park from OpenWeather API
    weather_data = get_weather_data(latitude, longitude, api_key)

    return render_template('game_viewer.html', weather_data=weather_data)

