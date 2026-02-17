import requests
from dotenv import load_dotenv
from pathlib import Path
import os
from ..database.creators.models import WeatherData, CityWeather, Current, DayForecast, Forecast, Alert
from ..database.servicesDb.databaseServ import saveWeatherData

#load_dotenv(Path(r"D:\python\cmi\final\CMI-2\cmi.env"))
load_dotenv(Path(r"E:\CMI-2\CMI-2\cmi.env"))
API_KEY_OPENCAGE = os.getenv("OPENCAGE_KEY")
API_KEY_WEATHER = os.getenv("WEATHERAPI_KEY")
if not API_KEY_OPENCAGE or not API_KEY_WEATHER:
    raise RuntimeError("Missing weather API keys in environment")

async def getWeather(cities):
    weather_data = {}
    for city in cities:
        place = f"{city}, Slovenia"

        response = requests.get(
            "https://api.opencagedata.com/geocode/v1/json",
            params={
                "q": place,
                "key": API_KEY_OPENCAGE,
                "limit": 1,
                "no_annotations": 1
            }
        )
        data = response.json()

        
        if not data.get("results"):
            print(f"[weather] No results for {city}, skipping...")
            continue
        
        coords = data["results"][0]["geometry"]
        location = f"{coords['lat']}, {coords['lng']}"


        BASE_URL = "http://api.weatherapi.com/v1/forecast.json"
        params = {
            "key": API_KEY_WEATHER,
            "q": location,
            "days": 3,
            "aqi": "yes",
            "alerts": "yes"
        }
        response = requests.get(BASE_URL, params=params)
        current = response.json()['current']
        currWeather = {
            "temp_c": current['temp_c'],
            "feelslike_c": current['feelslike_c'],
            "dewpoint_c": current['dewpoint_c'],
            "aqi": current['air_quality']['us-epa-index'],
            "icon": current['condition']['icon'],
            "condition": current['condition']['text'],
            "wind_kph": current['wind_kph'],
            "humidity": current['humidity'],
        }
        forecast = response.json()['forecast']['forecastday']
        forecastData = {
            "day1": {
                "date": forecast[0]['date'],
                "max_temp_c": forecast[0]['day']['maxtemp_c'],
                "min_temp_c": forecast[0]['day']['mintemp_c'],
                "avg_humidity": forecast[0]['day']['avghumidity'],
                "condition": forecast[0]['day']['condition']['text'],
                "icon": forecast[0]['day']['condition']['icon'],
                "total_precip_mm": forecast[0]['day']['totalprecip_mm'],
            },
            "day2": {
                "date": forecast[1]['date'],
                "max_temp_c": forecast[1]['day']['maxtemp_c'],
                "min_temp_c": forecast[1]['day']['mintemp_c'],
                "avg_humidity": forecast[1]['day']['avghumidity'],
                "condition": forecast[1]['day']['condition']['text'],
                "icon": forecast[1]['day']['condition']['icon'],
                "total_precip_mm": forecast[1]['day']['totalprecip_mm'],
            },
            "day3": {
                "date": forecast[2]['date'],
                "max_temp_c": forecast[2]['day']['maxtemp_c'],
                "min_temp_c": forecast[2]['day']['mintemp_c'],
                "avg_humidity": forecast[2]['day']['avghumidity'],
                "condition": forecast[2]['day']['condition']['text'],
                "icon": forecast[2]['day']['condition']['icon'],
                "total_precip_mm": forecast[2]['day']['totalprecip_mm'],
            }
        }
        alerts = response.json()['alerts']['alert']
        alertData = {}
        for alert in alerts:
            alertData[alert['headline']] = {
                "headline": alert['headline'],
                "msgtype": alert['msgtype'],
                "severity": alert['severity'],
                "urgency": alert['urgency'],
                "areas": alert['areas'],
                "category": alert['category'],
                "event": alert['event'],
                "instruction": alert['instruction'],
            }
            
        weather_data[city] = CityWeather(
            current=Current(**currWeather),
            forecast=Forecast(
                day1=DayForecast(**forecastData["day1"]),
                day2=DayForecast(**forecastData["day2"]),
                day3=DayForecast(**forecastData["day3"])
            ),
            alerts={key: Alert(**value) for key, value in alertData.items()}
        )
    weatherDataModel = WeatherData(
        weatherByCity=weather_data
    )
    await saveWeatherData(weatherDataModel)
    return weather_data

#todo, dej v bazo list mestou da ne klice usakic sprot kse spremeni ce pride novo mesto not in restarta weather.