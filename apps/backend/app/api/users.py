"""
User management API routes.
"""
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json

from ..core.database import get_db
from ..core.security import get_password_hash
from ..models.user import User
from ..schemas.user import User as UserSchema, UserCreate, UserUpdate, UserProfile
from .auth import get_current_user

router = APIRouter()


def create_user(db: Session, user: UserCreate):
    """Create a new user."""
    # Check if user already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        bio=user.bio,
        location=user.location,
        skills=json.dumps(user.skills),
        availability=json.dumps(user.availability),
        preferences=json.dumps(user.preferences)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return create_user(db=db, user=user)


@router.get("/profile/{username}", response_model=UserProfile)
def get_user_profile(username: str, db: Session = Depends(get_db)):
    """Get public user profile by username."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Parse JSON fields for response
    user_dict = user.__dict__.copy()
    for field in ['skills', 'availability']:
        if user_dict.get(field):
            try:
                user_dict[field] = json.loads(user_dict[field])
            except (json.JSONDecodeError, TypeError):
                user_dict[field] = []
        else:
            user_dict[field] = []
    
    return user_dict


@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    # Update fields
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field in ['skills', 'availability', 'preferences'] and value is not None:
            setattr(current_user, field, json.dumps(value))
        elif value is not None:
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    # Parse JSON fields for response
    user_dict = current_user.__dict__.copy()
    for field in ['skills', 'availability', 'preferences']:
        if user_dict.get(field):
            try:
                user_dict[field] = json.loads(user_dict[field])
            except (json.JSONDecodeError, TypeError):
                user_dict[field] = []
        else:
            user_dict[field] = []
    
    return user_dict