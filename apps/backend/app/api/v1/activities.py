from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.models import Activity, User, user_activity_registration
from app.schemas.activity import Activity as ActivitySchema, ActivityListResponse, ActivityRegistrationResponse
from app.core.deps import get_current_user
from datetime import datetime

router = APIRouter()


@router.get("/activities", response_model=ActivityListResponse)
async def list_activities(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    """List all activities with optional filtering by category"""
    query = db.query(Activity)
    
    if category:
        if category not in ["agri", "transfo", "artisanat", "nature", "social"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid category. Must be one of: agri, transfo, artisanat, nature, social"
            )
        query = query.filter(Activity.category == category)
    
    total = query.count()
    activities = query.offset(skip).limit(limit).all()
    
    return ActivityListResponse(activities=activities, total=total)


@router.get("/activities/{slug}", response_model=ActivitySchema)
async def get_activity_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get activity details by slug"""
    activity = db.query(Activity).filter(Activity.slug == slug).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    return activity


@router.post("/activities/{activity_id}/register", response_model=ActivityRegistrationResponse)
async def register_for_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register current user for an activity"""
    # Check if activity exists
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user is already registered
    existing_registration = db.query(user_activity_registration).filter(
        user_activity_registration.c.user_id == current_user.id,
        user_activity_registration.c.activity_id == activity_id
    ).first()
    
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already registered for this activity"
        )
    
    # Register user for activity
    registration_stmt = user_activity_registration.insert().values(
        user_id=current_user.id,
        activity_id=activity_id,
        registered_at=datetime.utcnow()
    )
    db.execute(registration_stmt)
    db.commit()
    
    return ActivityRegistrationResponse(
        message="Successfully registered for activity",
        activity_id=activity_id,
        user_id=current_user.id,
        registered_at=datetime.utcnow()
    )