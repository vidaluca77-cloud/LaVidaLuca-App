"""
Activity management endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.security import get_current_active_user
from ...models.user import User
from ...models.activity import Activity
from ...schemas.activity import (
    Activity as ActivitySchema, 
    ActivityCreate, 
    ActivityUpdate,
    ActivityList
)

router = APIRouter()


@router.post("/", response_model=ActivitySchema)
async def create_activity(
    activity_data: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new activity."""
    db_activity = Activity(
        **activity_data.dict(),
        creator_id=current_user.id
    )
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity


@router.get("/", response_model=ActivityList)
async def read_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = Query(None),
    difficulty_level: Optional[int] = Query(None, ge=1, le=5),
    is_active: bool = Query(True),
    is_featured: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all activities with optional filtering."""
    query = db.query(Activity)
    
    # Apply filters
    if is_active is not None:
        query = query.filter(Activity.is_active == is_active)
    
    if category:
        query = query.filter(Activity.category.ilike(f"%{category}%"))
    
    if difficulty_level:
        query = query.filter(Activity.difficulty_level == difficulty_level)
    
    if is_featured is not None:
        query = query.filter(Activity.is_featured == is_featured)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    activities = query.offset(skip).limit(limit).all()
    
    return ActivityList(
        activities=activities,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/{activity_id}", response_model=ActivitySchema)
async def read_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity


@router.put("/{activity_id}", response_model=ActivitySchema)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions: creator or admin can update
    if activity.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update activity data
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete an activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions: creator or admin can delete
    if activity.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(activity)
    db.commit()
    
    return {"message": "Activity deleted successfully"}


@router.get("/categories/", response_model=List[str])
async def get_activity_categories(db: Session = Depends(get_db)):
    """Get all unique activity categories."""
    categories = db.query(Activity.category).distinct().all()
    return [category[0] for category in categories if category[0]]