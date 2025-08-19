from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.activity import Activity
from app.schemas.activity import ActivityResponse, ActivityCreate, ActivityUpdate
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=List[ActivityResponse])
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    category: Optional[str] = Query(None),
    skill_tag: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of activities with optional filtering"""
    query = db.query(Activity)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if skill_tag:
        query = query.filter(Activity.skill_tags.contains([skill_tag]))
    
    activities = query.offset(skip).limit(limit).all()
    return [ActivityResponse.from_orm(activity) for activity in activities]


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(activity_id: str, db: Session = Depends(get_db)):
    """Get a specific activity by ID"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return ActivityResponse.from_orm(activity)


@router.post("/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_data: ActivityCreate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new activity (admin only)"""
    # TODO: Add admin check
    db_activity = Activity(
        slug=activity_data.slug,
        title=activity_data.title,
        category=activity_data.category,
        summary=activity_data.summary,
        duration_min=activity_data.duration_min,
        skill_tags=activity_data.skill_tags,
        seasonality=activity_data.seasonality,
        safety_level=activity_data.safety_level,
        materials=activity_data.materials,
        description=activity_data.description
    )
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    logger.info(f"New activity created: {activity_data.title}")
    return ActivityResponse.from_orm(db_activity)


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: str,
    activity_update: ActivityUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update an activity (admin only)"""
    # TODO: Add admin check
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Update fields if provided
    for field, value in activity_update.dict(exclude_unset=True).items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    logger.info(f"Activity updated: {activity.title}")
    return ActivityResponse.from_orm(activity)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete an activity (admin only)"""
    # TODO: Add admin check
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db.delete(activity)
    db.commit()
    
    logger.info(f"Activity deleted: {activity.title}")
    return


@router.get("/categories/", response_model=List[str])
async def get_activity_categories(db: Session = Depends(get_db)):
    """Get list of all activity categories"""
    categories = db.query(Activity.category).distinct().all()
    return [category[0] for category in categories]


@router.get("/skills/", response_model=List[str])
async def get_activity_skills(db: Session = Depends(get_db)):
    """Get list of all skill tags"""
    activities = db.query(Activity.skill_tags).all()
    skills = set()
    for activity in activities:
        if activity.skill_tags:
            skills.update(activity.skill_tags)
    return list(skills)