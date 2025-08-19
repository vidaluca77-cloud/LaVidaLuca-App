from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Location, UserRole
from schemas import (
    LocationCreate, LocationUpdate, LocationResponse,
    MessageResponse, PaginatedResponse
)
from routes.auth import get_current_active_user
from models import User

router = APIRouter()

def get_location_by_id(db: Session, location_id: int) -> Optional[Location]:
    """Get location by ID."""
    return db.query(Location).filter(Location.id == location_id).first()

def check_mentor_permission(current_user: User):
    """Check if user has mentor or admin permissions."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MENTOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

@router.get("/", response_model=PaginatedResponse)
async def list_locations(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    departement: Optional[str] = None,
    is_active: Optional[bool] = True,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List locations with filtering."""
    query = db.query(Location)
    
    # Apply filters
    if departement:
        query = query.filter(Location.departement.ilike(f"%{departement}%"))
    if is_active is not None:
        query = query.filter(Location.is_active == is_active)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Location.name.ilike(search_term) |
            Location.description.ilike(search_term) |
            Location.address.ilike(search_term)
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    locations = query.offset(offset).limit(size).all()
    
    return PaginatedResponse(
        items=[LocationResponse.from_orm(location) for location in locations],
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )

@router.get("/departements", response_model=List[str])
async def get_departements(
    db: Session = Depends(get_db)
):
    """Get all available departements."""
    result = db.query(Location.departement).filter(
        Location.departement.isnot(None),
        Location.is_active == True
    ).distinct().all()
    
    return [dept[0] for dept in result if dept[0]]

@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Create new location (mentor/admin only)."""
    check_mentor_permission(current_user)
    
    # Create location
    db_location = Location(**location_data.dict())
    
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    return db_location

@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    """Get location by ID."""
    location = get_location_by_id(db, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    return location

@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: int,
    location_update: LocationUpdate,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Update location (mentor/admin only)."""
    check_mentor_permission(current_user)
    
    location = get_location_by_id(db, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    # Update location fields
    update_data = location_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    
    db.commit()
    db.refresh(location)
    
    return location

@router.delete("/{location_id}", response_model=MessageResponse)
async def delete_location(
    location_id: int,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Deactivate location (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    location = get_location_by_id(db, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    location.is_active = False
    db.commit()
    
    return MessageResponse(message="Location deactivated successfully")

@router.post("/{location_id}/activate", response_model=MessageResponse)
async def activate_location(
    location_id: int,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Activate location (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    location = get_location_by_id(db, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    location.is_active = True
    db.commit()
    
    return MessageResponse(message="Location activated successfully")

@router.get("/{location_id}/activities", response_model=List[dict])
async def get_location_activities(
    location_id: int,
    db: Session = Depends(lambda: None),  # Will be injected properly
):
    """Get activities for a specific location."""
    location = get_location_by_id(db, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    # Return simplified activity list
    activities = []
    for activity in location.activities:
        if activity.is_active:
            activities.append({
                "id": activity.id,
                "slug": activity.slug,
                "title": activity.title,
                "category": activity.category.value,
                "duration_min": activity.duration_min,
                "safety_level": activity.safety_level.value
            })
    
    return activities