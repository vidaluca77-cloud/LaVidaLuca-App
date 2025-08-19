"""
Activities management API routes.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import json

from ..core.database import get_db
from ..models.activity import Activity
from ..schemas.activity import Activity as ActivitySchema, ActivityCreate, ActivityUpdate, ActivitySummary

router = APIRouter()


@router.get("/", response_model=List[ActivitySummary])
def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of activities with optional filtering."""
    query = db.query(Activity).filter(Activity.is_active == True)
    
    if category:
        query = query.filter(Activity.category == category)
    
    activities = query.offset(skip).limit(limit).all()
    
    # Parse JSON fields for response
    result = []
    for activity in activities:
        activity_dict = activity.__dict__.copy()
        for field in ['skill_tags', 'seasonality', 'materials']:
            if activity_dict.get(field):
                try:
                    activity_dict[field] = json.loads(activity_dict[field])
                except (json.JSONDecodeError, TypeError):
                    activity_dict[field] = []
            else:
                activity_dict[field] = []
        result.append(activity_dict)
    
    return result


@router.get("/{activity_id}", response_model=ActivitySchema)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id, Activity.is_active == True).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Parse JSON fields for response
    activity_dict = activity.__dict__.copy()
    for field in ['skill_tags', 'seasonality', 'materials']:
        if activity_dict.get(field):
            try:
                activity_dict[field] = json.loads(activity_dict[field])
            except (json.JSONDecodeError, TypeError):
                activity_dict[field] = []
        else:
            activity_dict[field] = []
    
    return activity_dict


@router.get("/slug/{slug}", response_model=ActivitySchema)
def get_activity_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get activity by slug."""
    activity = db.query(Activity).filter(Activity.slug == slug, Activity.is_active == True).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Parse JSON fields for response
    activity_dict = activity.__dict__.copy()
    for field in ['skill_tags', 'seasonality', 'materials']:
        if activity_dict.get(field):
            try:
                activity_dict[field] = json.loads(activity_dict[field])
            except (json.JSONDecodeError, TypeError):
                activity_dict[field] = []
        else:
            activity_dict[field] = []
    
    return activity_dict


@router.get("/categories/", response_model=List[str])
def get_activity_categories(db: Session = Depends(get_db)):
    """Get list of available activity categories."""
    categories = db.query(Activity.category).filter(Activity.is_active == True).distinct().all()
    return [category[0] for category in categories]