from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..db import models, schemas
from ..auth.auth_handler import get_current_active_user
from ..services.recommendation_service import ActivityRecommendationService

router = APIRouter()

@router.get("/", response_model=List[schemas.Activity])
async def read_activities(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None, description="Filter by category"),
    is_student_only: Optional[bool] = Query(None, description="Filter by student-only activities"),
    db: Session = Depends(get_db)
):
    """Get list of activities with optional filters."""
    query = db.query(models.Activity).filter(models.Activity.is_active == True)
    
    if category:
        query = query.filter(models.Activity.category == category)
    
    if is_student_only is not None:
        query = query.filter(models.Activity.is_student_only == is_student_only)
    
    activities = query.offset(skip).limit(limit).all()
    return activities

@router.get("/{activity_id}", response_model=schemas.Activity)
async def read_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get activity by ID."""
    activity = db.query(models.Activity).filter(
        models.Activity.id == activity_id,
        models.Activity.is_active == True
    ).first()
    
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity

@router.get("/slug/{slug}", response_model=schemas.Activity)
async def read_activity_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get activity by slug."""
    activity = db.query(models.Activity).filter(
        models.Activity.slug == slug,
        models.Activity.is_active == True
    ).first()
    
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity

@router.post("/", response_model=schemas.Activity, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity: schemas.ActivityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a new activity (admin function)."""
    # Check if slug already exists
    existing_activity = db.query(models.Activity).filter(models.Activity.slug == activity.slug).first()
    if existing_activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with this slug already exists"
        )
    
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity

@router.put("/{activity_id}", response_model=schemas.Activity)
async def update_activity(
    activity_id: int,
    activity_update: schemas.ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update an activity (admin function)."""
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_activity, field, value)
    
    db.commit()
    db.refresh(db_activity)
    
    return db_activity

@router.get("/recommendations/{user_id}", response_model=List[schemas.ActivityRecommendation])
async def get_activity_recommendations(
    user_id: int,
    category_filter: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(10, description="Number of recommendations to return"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get activity recommendations for a user."""
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get recommendations
    recommendation_service = ActivityRecommendationService(db)
    recommendations = recommendation_service.get_recommendations(
        user_id=user_id,
        category_filter=category_filter,
        limit=limit
    )
    
    return recommendations

@router.post("/{activity_id}/complete")
async def mark_activity_complete(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Mark an activity as completed by the current user."""
    # Check if activity exists
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if already completed
    existing_completion = db.query(models.user_activities).filter(
        models.user_activities.c.user_id == current_user.id,
        models.user_activities.c.activity_id == activity_id
    ).first()
    
    if existing_completion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity already marked as completed"
        )
    
    # Add completion record
    stmt = models.user_activities.insert().values(
        user_id=current_user.id,
        activity_id=activity_id
    )
    db.execute(stmt)
    db.commit()
    
    return {"message": "Activity marked as completed"}

@router.get("/categories/list")
async def get_activity_categories(db: Session = Depends(get_db)):
    """Get list of available activity categories."""
    categories = db.query(models.Activity.category).distinct().all()
    return [{"value": cat[0], "label": cat[0].title()} for cat in categories]