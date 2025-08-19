"""
User management API endpoints.
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...core.dependencies import standard_rate_limit
from ...core.security import get_current_active_user, require_admin, require_moderator
from ...db.session import get_db
from ...models.user import User
from ...schemas.user import User as UserSchema, UserUpdate, UserProfileUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserSchema])
@standard_rate_limit
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(require_moderator),
    db: Session = Depends(get_db)
):
    """List users (moderator and admin only)."""
    
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
@standard_rate_limit
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user by ID."""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Users can only see their own profile unless they're moderator+
    if user.id != current_user.id and not current_user.is_moderator_or_above:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return user


@router.put("/{user_id}", response_model=UserSchema)
@standard_rate_limit
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user information."""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Users can only update their own profile unless they're moderator+
    if user.id != current_user.id and not current_user.is_moderator_or_above:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.put("/profile", response_model=UserSchema)
@standard_rate_limit
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user profile data."""
    
    # Update profile_data field
    if current_user.profile_data is None:
        current_user.profile_data = {}
    
    update_data = profile_data.dict(exclude_unset=True)
    current_user.profile_data.update(update_data)
    
    # Also update location if provided
    if profile_data.location:
        current_user.location = profile_data.location
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.delete("/{user_id}")
@standard_rate_limit
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)."""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Cannot delete admin users
    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete admin users"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}


@router.post("/{user_id}/activate")
@standard_rate_limit
async def activate_user(
    user_id: UUID,
    current_user: User = Depends(require_moderator),
    db: Session = Depends(get_db)
):
    """Activate user account (moderator and admin only)."""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    db.commit()
    
    return {"message": "User activated successfully"}


@router.post("/{user_id}/deactivate")
@standard_rate_limit
async def deactivate_user(
    user_id: UUID,
    current_user: User = Depends(require_moderator),
    db: Session = Depends(get_db)
):
    """Deactivate user account (moderator and admin only)."""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Cannot deactivate admin users
    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate admin users"
        )
    
    user.is_active = False
    db.commit()
    
    return {"message": "User deactivated successfully"}