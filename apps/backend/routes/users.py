from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import User, UserRole
from schemas import (
    UserResponse, UserUpdate, MessageResponse, 
    PaginatedResponse, UserProfile
)
from routes.auth import get_current_active_user

router = APIRouter()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def check_admin_permission(current_user: User):
    """Check if user has admin permissions."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MENTOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

@router.get("/", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """List users (admin/mentor only)."""
    check_admin_permission(current_user)
    
    query = db.query(User)
    
    # Apply filters
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    users = query.offset(offset).limit(size).all()
    
    return PaginatedResponse(
        items=[UserResponse.from_orm(user) for user in users],
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID."""
    # Users can only see their own profile unless they're admin/mentor
    if user_id != current_user.id:
        check_admin_permission(current_user)
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Update user profile."""
    # Users can only update their own profile unless they're admin
    if user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Deactivate user account (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    db.commit()
    
    return MessageResponse(message="User deactivated successfully")

@router.post("/{user_id}/activate", response_model=MessageResponse)
async def activate_user(
    user_id: int,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Activate user account (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    db.commit()
    
    return MessageResponse(message="User activated successfully")

@router.get("/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Get user profile for AI matching."""
    # Users can only see their own profile unless they're admin/mentor
    if user_id != current_user.id:
        check_admin_permission(current_user)
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserProfile(
        skills=[],  # TODO: Implement skills relationship
        availability=user.availability or [],
        location=user.location or "",
        preferences=user.preferences or []
    )

@router.put("/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    new_role: UserRole,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Update user role (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.role = new_role
    db.commit()
    db.refresh(user)
    
    return user