from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.database import get_db
from app.models.models import User, Activity, Participation
from app.schemas.activity import Activity as ActivitySchema, ActivityCreate, ActivityUpdate, ActivityWithStats
from app.utils.auth import get_current_active_user, get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[ActivityWithStats])
def read_activities(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all activities with optional filtering."""
    query = db.query(Activity)
    
    if active_only:
        query = query.filter(Activity.is_active == True)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if search:
        query = query.filter(
            or_(
                Activity.title.ilike(f"%{search}%"),
                Activity.summary.ilike(f"%{search}%"),
                Activity.description.ilike(f"%{search}%")
            )
        )
    
    activities = query.offset(skip).limit(limit).all()
    
    # Add statistics for each activity
    activities_with_stats = []
    for activity in activities:
        participations = db.query(Participation).filter(Participation.activity_id == activity.id).all()
        participant_count = len(participations)
        
        # Calculate average rating
        ratings = [p.rating for p in participations if p.rating is not None]
        average_rating = sum(ratings) / len(ratings) if ratings else 0.0
        
        # Calculate completion rate
        completed = len([p for p in participations if p.status == "completed"])
        completion_rate = completed / participant_count if participant_count > 0 else 0.0
        
        activity_stats = ActivityWithStats(
            **activity.__dict__,
            participant_count=participant_count,
            average_rating=round(average_rating, 1),
            completion_rate=round(completion_rate * 100, 1)
        )
        activities_with_stats.append(activity_stats)
    
    return activities_with_stats


@router.get("/{activity_id}", response_model=ActivityWithStats)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Add statistics
    participations = db.query(Participation).filter(Participation.activity_id == activity.id).all()
    participant_count = len(participations)
    
    ratings = [p.rating for p in participations if p.rating is not None]
    average_rating = sum(ratings) / len(ratings) if ratings else 0.0
    
    completed = len([p for p in participations if p.status == "completed"])
    completion_rate = completed / participant_count if participant_count > 0 else 0.0
    
    return ActivityWithStats(
        **activity.__dict__,
        participant_count=participant_count,
        average_rating=round(average_rating, 1),
        completion_rate=round(completion_rate * 100, 1)
    )


@router.post("/", response_model=ActivitySchema)
def create_activity(
    activity: ActivityCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create new activity (admin only)."""
    # Check if slug already exists
    if db.query(Activity).filter(Activity.slug == activity.slug).first():
        raise HTTPException(status_code=400, detail="Activity slug already exists")
    
    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity


@router.put("/{activity_id}", response_model=ActivitySchema)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update activity (admin only)."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete activity (admin only)."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if activity has participations
    participations = db.query(Participation).filter(Participation.activity_id == activity_id).first()
    if participations:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete activity with existing participations"
        )
    
    db.delete(activity)
    db.commit()
    
    return {"message": "Activity deleted successfully"}


@router.get("/categories/list")
def get_categories():
    """Get list of available activity categories."""
    return {
        "categories": [
            {"id": "agri", "name": "Agriculture", "description": "Élevage, cultures, soins aux animaux"},
            {"id": "transfo", "name": "Transformation", "description": "Produits fermiers, cuisine, conservation"},
            {"id": "artisanat", "name": "Artisanat", "description": "Construction, réparation, création"},
            {"id": "nature", "name": "Environnement", "description": "Écologie, biodiversité, ressources"},
            {"id": "social", "name": "Animation", "description": "Accueil, pédagogie, événements"}
        ]
    }