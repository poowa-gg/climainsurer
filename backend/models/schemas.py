from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class TriggerType(str, Enum):
    RAINFALL = "rainfall"
    WIND_SPEED = "wind_speed"
    TEMPERATURE = "temperature"
    FLOOD_RISK = "flood_risk"
    DROUGHT = "drought"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Location(BaseModel):
    id: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    name: str
    insurer_id: str
    policy_ids: List[str] = []
    created_at: Optional[datetime] = None

class ParametricTrigger(BaseModel):
    id: Optional[str] = None
    location_id: str
    trigger_type: TriggerType
    threshold_value: float
    threshold_operator: str = Field(..., pattern="^(gt|lt|gte|lte|eq)$")
    duration_hours: int = 1
    active: bool = True
    payout_amount: Optional[float] = None

class WeatherData(BaseModel):
    location_id: str
    timestamp: datetime
    temperature: float
    rainfall: float
    wind_speed: float
    humidity: float
    pressure: float

class Alert(BaseModel):
    id: Optional[str] = None
    location_id: str
    trigger_id: str
    risk_level: RiskLevel
    message: str
    current_value: float
    threshold_value: float
    triggered_at: datetime
    resolved: bool = False
    prescriptive_actions: List[str] = []

class ForecastData(BaseModel):
    location_id: str
    forecast_time: datetime
    temperature: float
    rainfall_probability: float
    rainfall_amount: float
    wind_speed: float
    risk_score: float
    potential_triggers: List[str] = []
