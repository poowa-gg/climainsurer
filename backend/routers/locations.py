from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from ..models.schemas import Location

router = APIRouter()

# In-memory storage (replace with database)
locations_db = {}

@router.post("/", response_model=Location)
async def create_location(location: Location):
    """Register a new insured location"""
    location.id = str(uuid.uuid4())
    locations_db[location.id] = location
    return location

@router.get("/{location_id}", response_model=Location)
async def get_location(location_id: str):
    """Get location details"""
    if location_id not in locations_db:
        raise HTTPException(status_code=404, detail="Location not found")
    return locations_db[location_id]

@router.get("/", response_model=List[Location])
async def list_locations(insurer_id: str = None):
    """List all locations, optionally filtered by insurer"""
    if insurer_id:
        return [loc for loc in locations_db.values() if loc.insurer_id == insurer_id]
    return list(locations_db.values())
