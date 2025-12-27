from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    weather_api_key: str = os.getenv("WEATHER_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./hyperlocal.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    alert_webhook_url: Optional[str] = os.getenv("ALERT_WEBHOOK_URL")
    
    # Monitoring intervals
    check_interval_seconds: int = 300  # 5 minutes
    forecast_update_interval: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"

settings = Settings()
