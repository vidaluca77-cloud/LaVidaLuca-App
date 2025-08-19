from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..models.models import User, UserProfile
from ..schemas.schemas import User as UserSchema, UserUpdate, UserProfile as UserProfileSchema, UserProfileCreate, UserProfileUpdate
from ..auth.dependencies import get_current_active_user, get_current_admin_user
from ..core.logging import log_info

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserSchema)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's profile."""
    return current_user


@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's basic information."""
    # Update only provided fields
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    log_info(f"User updated profile: {current_user.email}")
    return current_user


@router.get("/me/profile", response_model=UserProfileSchema)
def get_current_user_detailed_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's detailed profile."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        # Create empty profile if it doesn't exist
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return profile


@router.post("/me/profile", response_model=UserProfileSchema)
def create_or_update_user_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create or update current user's detailed profile."""
    # Check if profile exists
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if existing_profile:
        # Update existing profile
        update_data = profile_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_profile, field, value)
        
        db.commit()
        db.refresh(existing_profile)
        log_info(f"User updated detailed profile: {current_user.email}")
        return existing_profile
    else:
        # Create new profile
        new_profile = UserProfile(
            user_id=current_user.id,
            **profile_data.dict()
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        log_info(f"User created detailed profile: {current_user.email}")
        return new_profile


@router.put("/me/profile", response_model=UserProfileSchema)
def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's detailed profile."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update only provided fields
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    log_info(f"User updated detailed profile: {current_user.email}")
    return profile


# Admin routes
@router.get("/", response_model=List[UserSchema])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
def get_user_by_id(
    user_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user_by_id(
    user_id: int,
    user_update: UserUpdate,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update only provided fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    log_info(f"Admin updated user: {user.email}")
    return user