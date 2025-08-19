from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User
from app.schemas.user import UserProfile, UserUpdate, UserActivitiesResponse
from app.core.deps import get_current_user

router = APIRouter()


@router.get("/users/me", response_model=UserProfile)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/users/me", response_model=UserProfile)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/users/me/activities", response_model=UserActivitiesResponse)
async def get_user_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of activities the current user is registered for"""
    # Refresh the user to ensure we have the latest registered activities
    db.refresh(current_user)
    
    activities = current_user.registered_activities
    total = len(activities)
    
    return UserActivitiesResponse(activities=activities, total=total)