from fastapi import APIRouter, HTTPException
from typing import List
from ..services.weather_service import WeatherService
from ..services.risk_engine import RiskEngine
from ..models.schemas import ForecastData, WeatherData
from ..routers.locations import locations_db
from ..routers.triggers import triggers_db

router = APIRouter()
weather_service = WeatherService()
risk_engine = RiskEngine()

@router.get("/{location_id}", response_model=List[ForecastData])
async def get_forecast(location_id: str):
    """Get hyperlocal forecast for a location"""
    if location_id not in locations_db:
        raise HTTPException(status_code=404, detail="Location not found")
    
    location = locations_db[location_id]
    forecasts = await weather_service.get_forecast(
        location.latitude,
        location.longitude,
        location_id
    )
    
    # Calculate risk scores
    location_triggers = [t for t in triggers_db.values() if t.location_id == location_id]
    for forecast in forecasts:
        forecast.risk_score = risk_engine.calculate_risk_score(forecast, location_triggers)
    
    return forecasts

@router.get("/{location_id}/current", response_model=WeatherData)
async def get_current_weather(location_id: str):
    """Get current weather for a location"""
    if location_id not in locations_db:
        raise HTTPException(status_code=404, detail="Location not found")
    
    location = locations_db[location_id]
    return await weather_service.get_current_weather(
        location.latitude,
        location.longitude,
        location_id
    )
