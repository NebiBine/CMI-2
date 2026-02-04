from fastapi import APIRouter, HTTPException, Response, Request, Form
from pydantic import BaseModel

router = APIRouter()

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    description: str

class WeatherRequest(BaseModel):
    location: str

@router.get('/getWeather', response_model=WeatherResponse)
async def getWeatherRoute(request:Request):
    return {"location": "Sample City", "temperature": 25.5, "description": "Sunny"}



