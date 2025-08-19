from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from database.models import User
from schemas.user import User as UserSchema, UserUpdate, UserProfile
from auth.security import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/me", response_model=UserSchema)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Update user fields
    user_data = user_update.dict(exclude_unset=True)
    for field, value in user_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/me/profile", response_model=UserProfile)
def get_user_profile(current_user: User = Depends(get_current_active_user)):
    return UserProfile(
        skills=current_user.skills or [],
        availability=current_user.availability or [],
        location=current_user.location or "",
        preferences=current_user.preferences or []
    )


@router.put("/me/profile", response_model=UserProfile)
def update_user_profile(
    profile: UserProfile,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    current_user.skills = profile.skills
    current_user.availability = profile.availability
    current_user.location = profile.location
    current_user.preferences = profile.preferences
    
    db.commit()
    db.refresh(current_user)
    
    return UserProfile(
        skills=current_user.skills or [],
        availability=current_user.availability or [],
        location=current_user.location or "",
        preferences=current_user.preferences or []
    )


@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users