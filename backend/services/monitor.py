import asyncio
from typing import List, Dict
from datetime import datetime
from .weather_service import WeatherService
from .risk_engine import RiskEngine
from ..models.schemas import Location, ParametricTrigger, Alert

class ParametricMonitor:
    def __init__(self):
        self.weather_service = WeatherService()
        self.risk_engine = RiskEngine()
        self.running = False
        self.task = None
        
        # In-memory storage (replace with database in production)
        self.locations: Dict[str, Location] = {}
        self.triggers: Dict[str, ParametricTrigger] = {}
        self.active_alerts: List[Alert] = []
    
    async def start(self):
        """Start monitoring loop"""
        self.running = True
        self.task = asyncio.create_task(self._monitor_loop())
    
    async def stop(self):
        """Stop monitoring loop"""
        self.running = False
        if self.task:
            self.task.cancel()
    
    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                await self._check_all_locations()
                await asyncio.sleep(300)  # Check every 5 minutes
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Monitor error: {e}")
                await asyncio.sleep(60)
    
    async def _check_all_locations(self):
        """Check all registered locations for trigger conditions"""
        for location in self.locations.values():
            try:
                weather = await self.weather_service.get_current_weather(
                    location.latitude,
                    location.longitude,
                    location.id
                )
                
                # Check all triggers for this location
                location_triggers = [
                    t for t in self.triggers.values() 
                    if t.location_id == location.id and t.active
                ]
                
                for trigger in location_triggers:
                    if self.risk_engine.evaluate_trigger(weather, trigger):
                        alert = self.risk_engine.create_alert(weather, trigger)
                        self.active_alerts.append(alert)
                        await self._send_alert_notification(alert)
                        
            except Exception as e:
                print(f"Error checking location {location.id}: {e}")
    
    async def _send_alert_notification(self, alert: Alert):
        """Send alert notification (webhook, email, etc.)"""
        print(f"ALERT: {alert.message} - Risk Level: {alert.risk_level}")
        # Implement webhook/notification logic here
