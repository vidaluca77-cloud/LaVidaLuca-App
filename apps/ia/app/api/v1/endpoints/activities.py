"""
Activities endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_active_user, get_current_superuser, get_optional_current_user
from app.models.models import Activity, User
from app.schemas.schemas import (
    Activity as ActivitySchema,
    ActivityCreate,
    ActivityUpdate,
    ActivityCategory
)

router = APIRouter()


@router.get("/", response_model=List[ActivitySchema])
async def list_activities(
    skip: int = 0,
    limit: int = 100,
    category: Optional[ActivityCategory] = None,
    difficulty: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    List activities with optional filtering
    """
    query = db.query(Activity)
    
    if active_only:
        query = query.filter(Activity.is_active == True)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if difficulty:
        query = query.filter(Activity.difficulty_level == difficulty)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/{activity_id}", response_model=ActivitySchema)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get activity by ID
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Only show active activities to non-admin users
    if not activity.is_active and (not current_user or not current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity


@router.get("/slug/{slug}", response_model=ActivitySchema)
async def get_activity_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get activity by slug
    """
    activity = db.query(Activity).filter(Activity.slug == slug).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Only show active activities to non-admin users
    if not activity.is_active and (not current_user or not current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity


@router.get("/categories/", response_model=List[str])
async def list_activity_categories():
    """
    List all available activity categories
    """
    return [category.value for category in ActivityCategory]


@router.get("/search/", response_model=List[ActivitySchema])
async def search_activities(
    q: str = Query(..., min_length=2, description="Search query"),
    category: Optional[ActivityCategory] = None,
    difficulty: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Search activities by title, summary, or skill tags
    """
    query = db.query(Activity).filter(Activity.is_active == True)
    
    # Search in title, summary, and skill_tags
    search_filter = (
        Activity.title.ilike(f"%{q}%") |
        Activity.summary.ilike(f"%{q}%") |
        Activity.description.ilike(f"%{q}%")
    )
    query = query.filter(search_filter)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if difficulty:
        query = query.filter(Activity.difficulty_level == difficulty)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


# Admin endpoints
@router.post("/", response_model=ActivitySchema)
async def create_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Create new activity (admin only)
    """
    # Check if slug already exists
    existing_activity = db.query(Activity).filter(Activity.slug == activity_data.slug).first()
    if existing_activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with this slug already exists"
        )
    
    db_activity = Activity(**activity_data.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity


@router.put("/{activity_id}", response_model=ActivitySchema)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Update activity (admin only)
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    update_data = activity_update.model_dump(exclude_unset=True)
    
    # Check if slug is being updated and if it conflicts
    if "slug" in update_data:
        existing_activity = db.query(Activity).filter(
            Activity.slug == update_data["slug"],
            Activity.id != activity_id
        ).first()
        if existing_activity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Activity with this slug already exists"
            )
    
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Delete activity (admin only) - soft delete by setting is_active to False
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    activity.is_active = False
    db.commit()
    
    return {"message": "Activity deleted successfully"}