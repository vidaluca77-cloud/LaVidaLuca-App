from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from database import get_db
from models import User, Skill, ActivitySuggestion
from schemas import (
    User as UserSchema, UserUpdate, ActivitySuggestion as ActivitySuggestionSchema,
    UserProfile
)
from routers.auth import get_current_active_user

router = APIRouter()

def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def parse_json_field(field_value):
    """Parse JSON field value, return list if valid JSON, otherwise empty list"""
    if not field_value:
        return []
    
    if isinstance(field_value, list):
        return field_value
    
    try:
        return json.loads(field_value)
    except (json.JSONDecodeError, TypeError):
        return []

@router.get("/me", response_model=UserSchema)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    
    # Get update data excluding unset fields
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Handle skills update
    if "skills" in update_data:
        skills = update_data.pop("skills")
        # Clear existing skills
        current_user.skills.clear()
        
        # Add new skills
        for skill_name in skills:
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if not skill:
                # Create skill if it doesn't exist
                skill = Skill(name=skill_name)
                db.add(skill)
            current_user.skills.append(skill)
    
    # Handle JSON fields
    if "availability" in update_data:
        current_user.availability = json.dumps(update_data.pop("availability"))
    
    if "preferences" in update_data:
        current_user.preferences = json.dumps(update_data.pop("preferences"))
    
    # Update other fields
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("/me/profile", response_model=UserProfile)
async def get_current_user_profile_formatted(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile in UserProfile format"""
    
    # Parse skills
    skills = [skill.name for skill in current_user.skills]
    
    # Parse availability and preferences from JSON
    availability = parse_json_field(current_user.availability)
    preferences = parse_json_field(current_user.preferences)
    
    return UserProfile(
        skills=skills,
        availability=availability,
        location=current_user.location or "",
        preferences=preferences
    )

@router.put("/me/profile", response_model=UserProfile)
async def update_current_user_profile_formatted(
    profile_update: UserProfile,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile using UserProfile format"""
    
    # Update skills
    current_user.skills.clear()
    for skill_name in profile_update.skills:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if not skill:
            skill = Skill(name=skill_name)
            db.add(skill)
        current_user.skills.append(skill)
    
    # Update other fields
    current_user.availability = json.dumps(profile_update.availability)
    current_user.preferences = json.dumps(profile_update.preferences)
    current_user.location = profile_update.location
    
    db.commit()
    db.refresh(current_user)
    
    return profile_update

@router.get("/me/suggestions", response_model=List[ActivitySuggestionSchema])
async def get_user_suggestions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's activity suggestions history"""
    suggestions = db.query(ActivitySuggestion).filter(
        ActivitySuggestion.user_id == current_user.id
    ).order_by(ActivitySuggestion.created_at.desc()).limit(20).all()
    
    return suggestions

@router.delete("/me/suggestions")
async def clear_user_suggestions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear user's activity suggestions history"""
    db.query(ActivitySuggestion).filter(
        ActivitySuggestion.user_id == current_user.id
    ).delete()
    
    db.commit()
    
    return {"message": "Suggestions cleared successfully"}

@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only or own profile)"""
    # Users can only view their own profile unless they're admin
    if user_id != current_user.id and not current_user.is_superuser:
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
    
    return user

@router.get("/", response_model=List[UserSchema])
async def get_users(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = db.query(User).all()
    return users

@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user (admin only or own profile)"""
    # Users can only update their own profile unless they're admin
    if user_id != current_user.id and not current_user.is_superuser:
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
    
    # Get update data excluding unset fields
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Handle skills update
    if "skills" in update_data:
        skills = update_data.pop("skills")
        user.skills.clear()
        
        for skill_name in skills:
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                db.add(skill)
            user.skills.append(skill)
    
    # Handle JSON fields
    if "availability" in update_data:
        user.availability = json.dumps(update_data.pop("availability"))
    
    if "preferences" in update_data:
        user.preferences = json.dumps(update_data.pop("preferences"))
    
    # Update other fields
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete user (admin only) - soft delete"""
    if not current_user.is_superuser:
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
    
    # Prevent self-deletion
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user.is_active = False
    db.commit()
    
    return {"message": "User deleted successfully"}