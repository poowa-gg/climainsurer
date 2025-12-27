from fastapi import APIRouter, HTTPException
from typing import List
from ..models.schemas import Alert, RiskLevel

router = APIRouter()

alerts_db = []

@router.get("/location/{location_id}", response_model=List[Alert])
async def get_location_alerts(location_id: str, active_only: bool = True):
    """Get alerts for a specific location"""
    alerts = [a for a in alerts_db if a.location_id == location_id]
    if active_only:
        alerts = [a for a in alerts if not a.resolved]
    return alerts

@router.get("/", response_model=List[Alert])
async def list_all_alerts(risk_level: RiskLevel = None, active_only: bool = True):
    """List all alerts with optional filtering"""
    alerts = alerts_db
    if active_only:
        alerts = [a for a in alerts if not a.resolved]
    if risk_level:
        alerts = [a for a in alerts if a.risk_level == risk_level]
    return alerts

@router.patch("/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    """Mark an alert as resolved"""
    alert = next((a for a in alerts_db if a.id == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.resolved = True
    return {"id": alert_id, "resolved": True}
