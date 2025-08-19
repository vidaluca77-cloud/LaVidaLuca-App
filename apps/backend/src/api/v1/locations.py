"""Location API routes."""

from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...api.deps import get_current_active_user, get_current_instructor_or_admin
from ...db.session import get_db
from ...models.location import Location
from ...models.user import User
from ...schemas.location import (
    Location as LocationSchema,
    LocationCreate,
    LocationUpdate,
    LocationWithActivities
)

router = APIRouter()


@router.get("/", response_model=List[LocationSchema])
def read_locations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Retrieve locations."""
    locations = db.query(Location).offset(skip).limit(limit).all()
    return locations


@router.post("/", response_model=LocationSchema)
def create_location(
    location_in: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Create new location."""
    db_location = Location(**location_in.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    return db_location


@router.get("/{location_id}", response_model=LocationWithActivities)
def read_location(
    location_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get location by ID with activities."""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.put("/{location_id}", response_model=LocationSchema)
def update_location(
    location_id: UUID,
    location_update: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Update location."""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    location_data = location_update.dict(exclude_unset=True)
    for field, value in location_data.items():
        setattr(location, field, value)
    
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@router.delete("/{location_id}")
def delete_location(
    location_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Delete location."""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Check if location has associated activities
    if location.activities:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete location with associated activities"
        )
    
    db.delete(location)
    db.commit()
    return {"message": "Location deleted successfully"}