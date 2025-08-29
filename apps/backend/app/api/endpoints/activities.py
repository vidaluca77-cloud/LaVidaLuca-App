from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...api.deps import get_current_active_user
from ...models.models import User, Activity
from ...schemas.schemas import ActivityCreate, ActivityUpdate, Activity as ActivitySchema


router = APIRouter()


@router.get("/", response_model=List[ActivitySchema], summary="Get activities list")
def get_activities(
    skip: int = Query(0, ge=0, description="Number of activities to skip (for pagination)"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of activities to return"),
    category: str = Query(None, description="Filter by activity category"),
    difficulty: str = Query(None, description="Filter by difficulty level", pattern="^(beginner|intermediate|advanced)$"),
    published_only: bool = Query(True, description="Only show published activities"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of learning activities.
    
    This endpoint supports filtering and pagination to help users find relevant activities.
    
    **Filtering options:**
    - **category**: Filter by activity category (e.g., agriculture, technology)
    - **difficulty**: Filter by difficulty level (beginner, intermediate, advanced)
    - **published_only**: Only return published activities (default: true)
    
    **Pagination:**
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (1-100, default: 100)
    
    Returns an array of activity objects with complete information.
    """
    query = db.query(Activity)
    
    if published_only:
        query = query.filter(Activity.is_published == True)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if difficulty:
        query = query.filter(Activity.difficulty_level == difficulty)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/{activity_id}", response_model=ActivitySchema, summary="Get activity by ID")
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Retrieve detailed information about a specific activity.
    
    Returns complete activity information including description, requirements,
    learning objectives, and metadata.
    
    - **activity_id**: The unique identifier of the activity
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/", response_model=ActivitySchema, summary="Create new activity")
def create_activity(
    activity: ActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new learning activity.
    
    **Authentication required.** Only authenticated users can create activities.
    The current user will be set as the creator of the activity.
    
    **Required fields:**
    - **title**: Activity title (max 255 characters)
    - **category**: Activity category
    
    **Optional fields:**
    - **description**: Detailed description of the activity
    - **difficulty_level**: beginner, intermediate, or advanced (default: beginner)
    - **duration_minutes**: Estimated duration in minutes
    - **location**: Where the activity takes place
    - **equipment_needed**: Required equipment or materials
    - **learning_objectives**: What participants will learn
    - **is_published**: Whether the activity is visible to others (default: false)
    
    Returns the created activity with generated ID and timestamps.
    """
    db_activity = Activity(**activity.dict(), creator_id=current_user.id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@router.put("/{activity_id}", response_model=ActivitySchema)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user owns the activity or is superuser
    if activity.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update fields
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    return activity


@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user owns the activity or is superuser
    if activity.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}


@router.get("/categories/", response_model=List[str], summary="Get activity categories")
def get_activity_categories(db: Session = Depends(get_db)):
    """
    Retrieve a list of all available activity categories.
    
    Returns a list of unique categories that are currently in use
    by published activities. This can be used to populate filter
    dropdowns or category selection forms.
    
    Categories may include:
    - agriculture
    - livestock  
    - forestry
    - environment
    - technology
    - business
    """
    categories = db.query(Activity.category).distinct().all()
    return [category[0] for category in categories if category[0]]