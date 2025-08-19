from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from ..db.database import get_db
from ..models.models import Activity, User, ActivityCategory, ActivityLevel
from ..schemas.schemas import Activity as ActivitySchema, ActivityCreate, ActivityUpdate, PaginatedResponse
from ..auth.dependencies import get_current_active_user, get_current_instructor_or_admin, optional_get_current_user
from ..core.logging import log_info

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/", response_model=List[ActivitySchema])
def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[ActivityCategory] = None,
    level: Optional[ActivityLevel] = None,
    search: Optional[str] = None,
    active_only: bool = True,
    current_user: Optional[User] = Depends(optional_get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of activities with optional filters."""
    query = db.query(Activity)
    
    # Filter by active status
    if active_only:
        query = query.filter(Activity.is_active == True)
    
    # Filter by category
    if category:
        query = query.filter(Activity.category == category)
    
    # Filter by level
    if level:
        query = query.filter(Activity.level == level)
    
    # Search in title and description
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Activity.title.ilike(search_term),
                Activity.description.ilike(search_term)
            )
        )
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/{activity_id}", response_model=ActivitySchema)
def get_activity(
    activity_id: int,
    current_user: Optional[User] = Depends(optional_get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if activity is active (unless user is instructor/admin)
    if not activity.is_active and (not current_user or current_user.role == "student"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity


@router.post("/", response_model=ActivitySchema, status_code=status.HTTP_201_CREATED)
def create_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_instructor_or_admin),
    db: Session = Depends(get_db)
):
    """Create a new activity (instructors and admins only)."""
    new_activity = Activity(
        instructor_id=current_user.id,
        **activity_data.dict()
    )
    
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    
    log_info(f"Activity created: {new_activity.title} by {current_user.email}")
    return new_activity


@router.put("/{activity_id}", response_model=ActivitySchema)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    current_user: User = Depends(get_current_instructor_or_admin),
    db: Session = Depends(get_db)
):
    """Update an activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user can edit this activity (own activity or admin)
    if current_user.role != "admin" and activity.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to edit this activity"
        )
    
    # Update only provided fields
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    log_info(f"Activity updated: {activity.title} by {current_user.email}")
    return activity


@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_instructor_or_admin),
    db: Session = Depends(get_db)
):
    """Delete (deactivate) an activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user can delete this activity (own activity or admin)
    if current_user.role != "admin" and activity.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this activity"
        )
    
    # Soft delete by setting is_active to False
    activity.is_active = False
    db.commit()
    
    log_info(f"Activity deleted: {activity.title} by {current_user.email}")
    return {"message": "Activity deleted successfully"}


@router.get("/instructor/{instructor_id}", response_model=List[ActivitySchema])
def get_activities_by_instructor(
    instructor_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    active_only: bool = True,
    current_user: Optional[User] = Depends(optional_get_current_user),
    db: Session = Depends(get_db)
):
    """Get activities by specific instructor."""
    # Verify instructor exists
    instructor = db.query(User).filter(User.id == instructor_id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    
    query = db.query(Activity).filter(Activity.instructor_id == instructor_id)
    
    # Filter by active status
    if active_only:
        query = query.filter(Activity.is_active == True)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/categories/", response_model=List[str])
def get_activity_categories():
    """Get list of available activity categories."""
    return [category.value for category in ActivityCategory]


@router.get("/levels/", response_model=List[str])
def get_activity_levels():
    """Get list of available activity levels."""
    return [level.value for level in ActivityLevel]