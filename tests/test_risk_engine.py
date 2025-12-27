import pytest
from datetime import datetime
from backend.services.risk_engine import RiskEngine
from backend.models.schemas import (
    WeatherData, ParametricTrigger, TriggerType, ForecastData
)

@pytest.fixture
def risk_engine():
    return RiskEngine()

@pytest.fixture
def sample_weather():
    return WeatherData(
        location_id="test-loc-1",
        timestamp=datetime.utcnow(),
        temperature=25.0,
        rainfall=30.0,
        wind_speed=15.0,
        humidity=70.0,
        pressure=1013.0
    )

@pytest.fixture
def rainfall_trigger():
    return ParametricTrigger(
        id="trigger-1",
        location_id="test-loc-1",
        trigger_type=TriggerType.RAINFALL,
        threshold_value=25.0,
        threshold_operator="gt",
        duration_hours=1,
        active=True
    )

def test_evaluate_trigger_rainfall_exceeds(risk_engine, sample_weather, rainfall_trigger):
    result = risk_engine.evaluate_trigger(sample_weather, rainfall_trigger)
    assert result is True

def test_evaluate_trigger_rainfall_below(risk_engine, rainfall_trigger):
    weather = WeatherData(
        location_id="test-loc-1",
        timestamp=datetime.utcnow(),
        temperature=25.0,
        rainfall=20.0,
        wind_speed=15.0,
        humidity=70.0,
        pressure=1013.0
    )
    result = risk_engine.evaluate_trigger(weather, rainfall_trigger)
    assert result is False

def test_create_alert(risk_engine, sample_weather, rainfall_trigger):
    alert = risk_engine.create_alert(sample_weather, rainfall_trigger)
    assert alert.location_id == "test-loc-1"
    assert alert.trigger_id == "trigger-1"
    assert alert.current_value == 30.0
    assert len(alert.prescriptive_actions) > 0
