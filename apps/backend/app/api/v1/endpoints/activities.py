from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Activity as ActivityModel, ActivityCategory, ActivityDifficulty
from app.schemas import (
    Activity, ActivityCreate, ActivityUpdate, ActivityWithCreator
)
from .users import get_current_active_user, UserModel

router = APIRouter()


@router.post("/", response_model=Activity, status_code=status.HTTP_201_CREATED)
def create_activity(
    activity_data: ActivityCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new activity (authenticated users only)"""
    # Create new activity
    db_activity = ActivityModel(
        title=activity_data.title,
        description=activity_data.description,
        category=activity_data.category,
        difficulty=activity_data.difficulty,
        duration_hours=activity_data.duration_hours,
        materials_needed=activity_data.materials_needed,
        prerequisites=activity_data.prerequisites,
        learning_objectives=activity_data.learning_objectives,
        location_type=activity_data.location_type,
        max_participants=activity_data.max_participants,
        is_featured=activity_data.is_featured,
        created_by=current_user.id
    )
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity


@router.get("/", response_model=List[Activity])
def list_activities(
    skip: int = 0,
    limit: int = 100,
    category: Optional[ActivityCategory] = Query(None, description="Filter by category"),
    difficulty: Optional[ActivityDifficulty] = Query(None, description="Filter by difficulty"),
    featured_only: bool = Query(False, description="Show only featured activities"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    db: Session = Depends(get_db)
):
    """List activities with optional filters"""
    query = db.query(ActivityModel).filter(ActivityModel.is_active == True)
    
    # Apply filters
    if category:
        query = query.filter(ActivityModel.category == category)
    
    if difficulty:
        query = query.filter(ActivityModel.difficulty == difficulty)
    
    if featured_only:
        query = query.filter(ActivityModel.is_featured == True)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (ActivityModel.title.ilike(search_term)) |
            (ActivityModel.description.ilike(search_term))
        )
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/{activity_id}", response_model=ActivityWithCreator)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    """Get activity by ID with creator information"""
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id,
        ActivityModel.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Add creator info (basic info only for privacy)
    activity_dict = activity.__dict__.copy()
    if activity.creator:
        activity_dict["creator"] = {
            "id": activity.creator.id,
            "username": activity.creator.username,
            "full_name": activity.creator.full_name,
            "school": activity.creator.school
        }
    
    return activity_dict


@router.put("/{activity_id}", response_model=Activity)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update activity (only by creator or admin)"""
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id,
        ActivityModel.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permission (creator or admin)
    if activity.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update activity
    update_data = activity_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activity_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete activity (soft delete - only by creator or admin)"""
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id,
        ActivityModel.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permission (creator or admin)
    if activity.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Soft delete
    activity.is_active = False
    db.commit()


@router.get("/categories/", response_model=List[str])
def get_activity_categories():
    """Get all available activity categories"""
    return [category.value for category in ActivityCategory]


@router.get("/difficulties/", response_model=List[str])
def get_activity_difficulties():
    """Get all available difficulty levels"""
    return [difficulty.value for difficulty in ActivityDifficulty]


@router.get("/featured/", response_model=List[Activity])
def get_featured_activities(
    limit: int = Query(6, description="Number of featured activities to return"),
    db: Session = Depends(get_db)
):
    """Get featured activities for homepage"""
    activities = db.query(ActivityModel).filter(
        ActivityModel.is_active == True,
        ActivityModel.is_featured == True
    ).limit(limit).all()
    
    return activities