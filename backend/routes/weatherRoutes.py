from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel
from ..database.creators.models import WeatherData
from ..database.servicesDb.databaseServ import getWeatherData, getCityId

router = APIRouter()

class WeatherResponse(BaseModel):
    weather: WeatherData

@router.get('/getWeather', response_model=WeatherResponse)
async def getWeatherRoute(request:Request):
    userId = request.cookies.get("sessionId")
    if not userId:
        raise HTTPException(status_code=401, detail="Unauthorized, ni idja")    
    city = await getCityId(userId)
    weatherData = await getWeatherData(city)
    if not weatherData:
        raise HTTPException(status_code=404, detail="Weather data not found for the city")
    return {"weather": weatherData}



