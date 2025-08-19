import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.crud.crud import get_activity, get_activities, create_activity, update_activity, get_activity_by_slug
from app.schemas.schemas import Activity, ActivityCreate, ActivityUpdate
from app.models.models import User as UserModel

router = APIRouter()

def convert_activity_data(activity):
    """Convert JSON strings back to lists for API response"""
    if activity:
        if activity.skill_tags:
            activity.skill_tags = json.loads(activity.skill_tags) if isinstance(activity.skill_tags, str) else activity.skill_tags
        if activity.seasonality:
            activity.seasonality = json.loads(activity.seasonality) if isinstance(activity.seasonality, str) else activity.seasonality
        if activity.materials:
            activity.materials = json.loads(activity.materials) if isinstance(activity.materials, str) else activity.materials
    return activity

@router.get("/", response_model=List[Activity])
def read_activities(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    activities = get_activities(db, skip=skip, limit=limit, category=category)
    return [convert_activity_data(activity) for activity in activities]

@router.get("/{activity_id}", response_model=Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = get_activity(db, activity_id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return convert_activity_data(db_activity)

@router.get("/slug/{slug}", response_model=Activity)
def read_activity_by_slug(slug: str, db: Session = Depends(get_db)):
    db_activity = get_activity_by_slug(db, slug=slug)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return convert_activity_data(db_activity)

@router.post("/", response_model=Activity)
def create_activity_endpoint(
    activity: ActivityCreate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    # Only superusers can create activities
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    # Check if activity with this slug already exists
    if get_activity_by_slug(db, slug=activity.slug):
        raise HTTPException(
            status_code=400,
            detail="Activity with this slug already exists"
        )
    
    db_activity = create_activity(db=db, activity=activity)
    return convert_activity_data(db_activity)

@router.put("/{activity_id}", response_model=Activity)
def update_activity_endpoint(
    activity_id: int, 
    activity_update: ActivityUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    # Only superusers can update activities
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    updated_activity = update_activity(db, activity_id=activity_id, activity_update=activity_update)
    if updated_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return convert_activity_data(updated_activity)