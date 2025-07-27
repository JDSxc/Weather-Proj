import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from weather_code_info import weather_code_desc
from secrets_helper import get_api_key

@dataclass
class current_weather_data:
    temp: float
    windspeed: float
    weathercode: int
    description: str
    icon: str

@dataclass
class forecast_data:
    dates: list[str]
    temps_max: list[float]
    temps_min: list[float]
    weathercodes: list[int]
    descriptions: list[str]
    icons: str

api_key = get_api_key()

# This function will get lat and long based on city name, state code, and country name).
def get_lat_long(city_name, state_code, country_name, api_key):
    resp = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code}"
    f",{country_name}&appid={api_key}").json()

    if not resp:
        return None, None

    data = resp[0]
    lat = data.get('lat')
    long = data.get('lon')
    return lat, long

# This function will get current weather information based on lat and long.
def get_current_weather(lat, long):
    resp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&"
    f"current_weather=true&timezone=auto&temperature_unit=fahrenheit&wind_speed_unit=mph").json()

    current_weather_code = resp.get('current_weather').get('weathercode')

    data = current_weather_data(
            temp=resp.get('current_weather').get('temperature'),
            windspeed=resp.get('current_weather').get('windspeed'),
            weathercode=current_weather_code,
            description=weather_code_desc.get(current_weather_code, 'Unknown'),
            icon=get_icon(current_weather_code)
    )

    return data

# This will get 8-day forecast information based on the lat and long.
def get_forecast(lat, long):
    resp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&"
    f"daily=temperature_2m_max,temperature_2m_min,weather_code&forecast_days=8&timezone=auto&"
    f"temperature_unit=fahrenheit").json()

    forecast_weather_codes = resp.get('daily').get('weather_code')

    data = forecast_data(
            dates=resp.get('daily').get('time'),
            temps_max=resp.get('daily').get('temperature_2m_max'),
            temps_min=resp.get('daily').get('temperature_2m_min'),
            weathercodes=forecast_weather_codes,
            descriptions=[weather_code_desc.get(code, 'Unknown') for code in forecast_weather_codes],
            icons=[get_icon(code) for code in forecast_weather_codes]
    )

    return data

# This will get icon from location.
def get_icon(weather_code: int, extension="png") -> str:
    return f"static/icons/{weather_code}.{extension}"

# Main
def main(city_name, state_code, country_name):
    lat, long = get_lat_lon(city_name, state_code, country_name, api_key)
    current_weather_data = get_current_weather(lat, long)
    forecast_data = get_forecast(lat, long)
    return current_weather_data, forecast_data

# This is for just testing weather.py
if __name__ == "__main__":
    lat, long = get_lat_long('San Antonio', 'Tx', 'United States', api_key)
    current_weather_data = get_current_weather(lat, long)
    forecast_data = get_forecast(lat, long)
    print(current_weather_data)
    print()
    print(forecast_data)
