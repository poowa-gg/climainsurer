from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from ..models.schemas import ParametricTrigger

router = APIRouter()

triggers_db = {}

@router.post("/", response_model=ParametricTrigger)
async def create_trigger(trigger: ParametricTrigger):
    """Create a new parametric trigger"""
    trigger.id = str(uuid.uuid4())
    triggers_db[trigger.id] = trigger
    return trigger

@router.get("/{trigger_id}", response_model=ParametricTrigger)
async def get_trigger(trigger_id: str):
    """Get trigger details"""
    if trigger_id not in triggers_db:
        raise HTTPException(status_code=404, detail="Trigger not found")
    return triggers_db[trigger_id]

@router.get("/location/{location_id}", response_model=List[ParametricTrigger])
async def list_location_triggers(location_id: str):
    """List all triggers for a location"""
    return [t for t in triggers_db.values() if t.location_id == location_id]

@router.patch("/{trigger_id}/toggle")
async def toggle_trigger(trigger_id: str):
    """Activate or deactivate a trigger"""
    if trigger_id not in triggers_db:
        raise HTTPException(status_code=404, detail="Trigger not found")
    trigger = triggers_db[trigger_id]
    trigger.active = not trigger.active
    return {"id": trigger_id, "active": trigger.active}
