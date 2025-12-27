import httpx
from typing import Dict, List
from datetime import datetime, timedelta
from ..models.schemas import WeatherData, ForecastData
from ..config import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.weather_api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(self, lat: float, lon: float, location_id: str) -> WeatherData:
        """Fetch current weather data for a location"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            data = response.json()
            
            return WeatherData(
                location_id=location_id,
                timestamp=datetime.utcnow(),
                temperature=data["main"]["temp"],
                rainfall=data.get("rain", {}).get("1h", 0.0),
                wind_speed=data["wind"]["speed"],
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"]
            )
    
    async def get_forecast(self, lat: float, lon: float, location_id: str) -> List[ForecastData]:
        """Fetch 5-day forecast with 3-hour intervals"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/forecast",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            data = response.json()
            
            forecasts = []
            for item in data["list"][:16]:  # Next 48 hours
                forecasts.append(ForecastData(
                    location_id=location_id,
                    forecast_time=datetime.fromtimestamp(item["dt"]),
                    temperature=item["main"]["temp"],
                    rainfall_probability=item.get("pop", 0.0) * 100,
                    rainfall_amount=item.get("rain", {}).get("3h", 0.0),
                    wind_speed=item["wind"]["speed"],
                    risk_score=0.0,  # Calculated by risk engine
                    potential_triggers=[]
                ))
            
            return forecasts
