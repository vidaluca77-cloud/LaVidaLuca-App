from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...core.database import get_db
from ...models.activity import Activity
from ...models.user import User
from ...schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse
from .users import get_current_user

router = APIRouter()

@router.post("/", response_model=ActivityResponse)
def create_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new activity (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if slug already exists
    existing_activity = db.query(Activity).filter(Activity.slug == activity_data.slug).first()
    if existing_activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with this slug already exists"
        )
    
    # Create new activity
    db_activity = Activity(**activity_data.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity

@router.get("/", response_model=List[ActivityResponse])
def get_activities(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None, description="Filter by category"),
    skill_tags: Optional[str] = Query(None, description="Filter by skill tags (comma-separated)"),
    mfr_only: Optional[bool] = Query(None, description="Filter MFR-only activities"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all activities with optional filtering"""
    query = db.query(Activity).filter(Activity.is_active == True)
    
    # Apply filters
    if category:
        query = query.filter(Activity.category == category)
    
    if skill_tags:
        tags = [tag.strip() for tag in skill_tags.split(",")]
        for tag in tags:
            query = query.filter(Activity.skill_tags.contains([tag]))
    
    if mfr_only is not None:
        query = query.filter(Activity.is_mfr_only == mfr_only)
    
    # If user is not MFR student/educator, hide MFR-only activities
    if current_user.user_type not in ["mfr_student", "educator", "admin"]:
        query = query.filter(Activity.is_mfr_only == False)
    
    activities = query.offset(skip).limit(limit).all()
    return activities

@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get activity by ID"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check access to MFR-only activities
    if activity.is_mfr_only and current_user.user_type not in ["mfr_student", "educator", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This activity is reserved for MFR students"
        )
    
    return activity

@router.get("/slug/{slug}", response_model=ActivityResponse)
def get_activity_by_slug(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get activity by slug"""
    activity = db.query(Activity).filter(Activity.slug == slug).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check access to MFR-only activities
    if activity.is_mfr_only and current_user.user_type not in ["mfr_student", "educator", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This activity is reserved for MFR students"
        )
    
    return activity

@router.put("/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update activity (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity

@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete activity (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Soft delete
    activity.is_active = False
    db.commit()
    
    return {"message": "Activity deleted successfully"}

@router.get("/categories/", response_model=List[str])
def get_activity_categories():
    """Get all available activity categories"""
    return ["agri", "transfo", "artisanat", "nature", "social"]