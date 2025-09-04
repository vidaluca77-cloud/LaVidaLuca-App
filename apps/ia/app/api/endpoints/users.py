"""
User profiles API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_active_user
from app.models.models import User
from app.schemas.schemas import (
    User as UserSchema,
    UserUpdate,
    APIResponse
)

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def get_my_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user's profile"""
    return current_user

@router.put("/me", response_model=APIResponse)
async def update_my_profile(
    profile_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    
    # Check if username or email is already taken by another user
    if profile_update.username:
        existing_user = db.query(User).filter(
            User.username == profile_update.username,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    if profile_update.email:
        existing_user = db.query(User).filter(
            User.email == profile_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
    
    # Update user fields
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field in ['skills', 'availability', 'preferences']:
            # Handle array fields specially if needed
            setattr(current_user, field, value)
        else:
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return APIResponse(
        success=True,
        message="Profile updated successfully"
    )

@router.get("/{user_id}", response_model=UserSchema)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get another user's profile (public information only)"""
    
    user = db.query(User).filter(
        User.id == user_id,
        User.is_active == True
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Return limited public profile
    return UserSchema(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        location=user.location,
        is_mfr_student=user.is_mfr_student,
        email="",  # Don't expose email
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        skills=[],  # Don't expose detailed skills
        availability=[],  # Don't expose availability
        preferences=[]  # Don't expose preferences
    )