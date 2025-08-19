"""
Activities API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_active_user
from app.models.models import Activity as ActivityModel, User
from app.schemas.schemas import (
    Activity,
    ActivityCreate,
    ActivityUpdate,
    ActivityCategory,
    PaginatedResponse,
    APIResponse
)

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[ActivityCategory] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Get list of activities with pagination and filtering"""
    
    query = db.query(ActivityModel).filter(ActivityModel.is_active == is_active)
    
    if category:
        query = query.filter(ActivityModel.category == category)
    
    total = query.count()
    activities = query.offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=activities,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@router.get("/{activity_id}", response_model=Activity)
async def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get a specific activity by ID"""
    
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id,
        ActivityModel.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity

@router.get("/slug/{slug}", response_model=Activity)
async def get_activity_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get a specific activity by slug"""
    
    activity = db.query(ActivityModel).filter(
        ActivityModel.slug == slug,
        ActivityModel.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity

@router.post("/", response_model=APIResponse)
async def create_activity(
    activity_data: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new activity (admin only)"""
    
    # Check if slug already exists
    existing_activity = db.query(ActivityModel).filter(
        ActivityModel.slug == activity_data.slug
    ).first()
    
    if existing_activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with this slug already exists"
        )
    
    # Create new activity
    db_activity = ActivityModel(**activity_data.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return APIResponse(
        success=True,
        message="Activity created successfully",
        data={"activity_id": db_activity.id}
    )

@router.put("/{activity_id}", response_model=APIResponse)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an activity (admin only)"""
    
    activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Update activity fields
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return APIResponse(
        success=True,
        message="Activity updated successfully",
        data={"activity_id": activity.id}
    )

@router.delete("/{activity_id}", response_model=APIResponse)
async def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Soft delete an activity (admin only)"""
    
    activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Soft delete
    activity.is_active = False
    db.commit()
    
    return APIResponse(
        success=True,
        message="Activity deleted successfully"
    )

@router.get("/categories/list", response_model=List[str])
async def get_activity_categories():
    """Get list of available activity categories"""
    return [category.value for category in ActivityCategory]