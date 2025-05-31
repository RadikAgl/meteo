import requests
import openmeteo_requests

import requests_cache
from retry_requests import retry
import pandas as pd

import datetime


def get_time(timestamps):
    """Извлекает время из временной метки"""
    return datetime.datetime.fromtimestamp(int(timestamps)).strftime('%H:%M')


def get_city_geodata(city_name: str) -> tuple[bool, dict]:
    """Получение геоданных по названию города"""
    try:
        city = requests.get(url='https://geocoding-api.open-meteo.com/v1/search?name=' + city_name)
        location_data = city.json()
        result = True
    except Exception:
        location_data = {}
        result = False
    return result, location_data


def get_coords(data: dict) -> dict:
    """Извлечение координат локации"""

    longitude = data[1]['results'][0]['longitude']
    latitude = data[1]['results'][0]['latitude']

    return {"longitude": longitude, "latitude": latitude}


def get_timezone(data: dict) -> str:
    """Получение часового пояса местности"""
    return data[1]['results'][0]['timezone']


def get_forecast_data(response) -> pd.DataFrame:
    """Извлечение данных погоды на несколько дней"""
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(2).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(3).ValuesAsNumpy()
    daily_sunrise = daily.Variables(4).ValuesInt64AsNumpy()
    daily_sunset = daily.Variables(5).ValuesInt64AsNumpy()
    daily_precipitation_probability_max = daily.Variables(6).ValuesAsNumpy()
    daily_surface_pressure_mean = daily.Variables(7).ValuesAsNumpy()
    daily_relative_humidity_2m_mean = daily.Variables(8).ValuesAsNumpy()

    date = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )

    daily_data = {}
    daily_data["date"] = date
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["sunrise"] = [get_time(d) for d in daily_sunrise]
    daily_data["sunset"] = [get_time(d) for d in daily_sunset]
    daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
    daily_data["surface_pressure_mean"] = daily_surface_pressure_mean
    daily_data["relative_humidity_2m_mean"] = daily_relative_humidity_2m_mean
    daily_dataframe = pd.DataFrame(data=daily_data)

    return daily_dataframe


def get_weather(city_name: str):
    """Запрос погоды и обработка"""
    # Set up the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    data = get_city_geodata(city_name)
    coords = get_coords(data)
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "daily": ["weather_code", "temperature_2m_min", "temperature_2m_max", "wind_speed_10m_max", "sunrise", "sunset",
                  "precipitation_probability_max", "surface_pressure_mean", "relative_humidity_2m_mean"],
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "precipitation", "surface_pressure"],
        "timezone": get_timezone(data)
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_wind_speed_10m = current.Variables(2).Value()
    current_precipitation = current.Variables(3).Value()
    current_surface_pressure = current.Variables(4).Value()

    res = {}
    current_data = {}

    current_data["time"] = current.Time()
    current_data["temperature"] = current_temperature_2m
    current_data["relative_humidity"] = current_relative_humidity_2m
    current_data["wind_speed"] = current_wind_speed_10m
    current_data["precipitation"] = current_precipitation
    current_data["surface_pressure"] = current_surface_pressure

    res["current"] = current_data

    daily_dataframe = get_forecast_data(response)

    res["daily"] = daily_dataframe.to_dict("records")
    return res
