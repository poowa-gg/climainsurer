from typing import List, Dict
from ..models.schemas import (
    WeatherData, ForecastData, ParametricTrigger, 
    Alert, RiskLevel, TriggerType
)
from datetime import datetime
import uuid

class RiskEngine:
    def __init__(self):
        self.prescriptive_actions = {
            TriggerType.RAINFALL: [
                "Deploy emergency drainage equipment",
                "Alert policyholders in affected area",
                "Prepare claims processing team",
                "Activate flood response protocol"
            ],
            TriggerType.WIND_SPEED: [
                "Issue high wind warning to policyholders",
                "Pre-position damage assessment teams",
                "Review building coverage limits",
                "Activate storm response protocol"
            ],
            TriggerType.TEMPERATURE: [
                "Monitor for heat/cold damage claims",
                "Alert agricultural policyholders",
                "Review temperature-sensitive policies"
            ],
            TriggerType.FLOOD_RISK: [
                "Evacuate high-risk areas if needed",
                "Deploy flood barriers",
                "Activate emergency claims hotline"
            ]
        }
    
    def evaluate_trigger(
        self, 
        weather: WeatherData, 
        trigger: ParametricTrigger
    ) -> bool:
        """Check if weather data triggers a parametric condition"""
        value_map = {
            TriggerType.RAINFALL: weather.rainfall,
            TriggerType.WIND_SPEED: weather.wind_speed,
            TriggerType.TEMPERATURE: weather.temperature
        }
        
        current_value = value_map.get(trigger.trigger_type)
        if current_value is None:
            return False
        
        operators = {
            "gt": lambda x, y: x > y,
            "lt": lambda x, y: x < y,
            "gte": lambda x, y: x >= y,
            "lte": lambda x, y: x <= y,
            "eq": lambda x, y: x == y
        }
        
        op = operators.get(trigger.threshold_operator)
        return op(current_value, trigger.threshold_value) if op else False
    
    def calculate_risk_score(self, forecast: ForecastData, triggers: List[ParametricTrigger]) -> float:
        """Calculate risk score based on forecast and active triggers"""
        risk_score = 0.0
        
        # Base risk from weather conditions
        if forecast.rainfall_amount > 50:
            risk_score += 0.4
        elif forecast.rainfall_amount > 25:
            risk_score += 0.2
        
        if forecast.wind_speed > 20:
            risk_score += 0.3
        elif forecast.wind_speed > 15:
            risk_score += 0.15
        
        # Additional risk from proximity to trigger thresholds
        for trigger in triggers:
            if trigger.trigger_type == TriggerType.RAINFALL:
                proximity = forecast.rainfall_amount / trigger.threshold_value
                if proximity > 0.7:
                    risk_score += 0.3
            elif trigger.trigger_type == TriggerType.WIND_SPEED:
                proximity = forecast.wind_speed / trigger.threshold_value
                if proximity > 0.7:
                    risk_score += 0.3
        
        return min(risk_score, 1.0)
    
    def create_alert(
        self, 
        weather: WeatherData, 
        trigger: ParametricTrigger
    ) -> Alert:
        """Generate alert when trigger is activated"""
        value_map = {
            TriggerType.RAINFALL: weather.rainfall,
            TriggerType.WIND_SPEED: weather.wind_speed,
            TriggerType.TEMPERATURE: weather.temperature
        }
        
        current_value = value_map.get(trigger.trigger_type, 0.0)
        risk_level = self._determine_risk_level(current_value, trigger.threshold_value)
        
        return Alert(
            id=str(uuid.uuid4()),
            location_id=trigger.location_id,
            trigger_id=trigger.id,
            risk_level=risk_level,
            message=f"{trigger.trigger_type.value} threshold exceeded: {current_value} {trigger.threshold_operator} {trigger.threshold_value}",
            current_value=current_value,
            threshold_value=trigger.threshold_value,
            triggered_at=datetime.utcnow(),
            prescriptive_actions=self.prescriptive_actions.get(trigger.trigger_type, [])
        )
    
    def _determine_risk_level(self, current: float, threshold: float) -> RiskLevel:
        """Determine risk level based on how much threshold is exceeded"""
        ratio = current / threshold if threshold > 0 else 0
        
        if ratio >= 1.5:
            return RiskLevel.CRITICAL
        elif ratio >= 1.2:
            return RiskLevel.HIGH
        elif ratio >= 1.0:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
