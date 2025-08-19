from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...api.deps import get_current_active_user
from ...models.models import User, Activity
from ...schemas.schemas import ActivityCreate, ActivityUpdate, Activity as ActivitySchema


router = APIRouter()


@router.get("/", response_model=List[ActivitySchema])
def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: str = None,
    difficulty: str = None,
    published_only: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(Activity)
    
    if published_only:
        query = query.filter(Activity.is_published == True)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if difficulty:
        query = query.filter(Activity.difficulty_level == difficulty)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/{activity_id}", response_model=ActivitySchema)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/", response_model=ActivitySchema)
def create_activity(
    activity: ActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
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


@router.get("/categories/", response_model=List[str])
def get_activity_categories(db: Session = Depends(get_db)):
    categories = db.query(Activity.category).distinct().all()
    return [category[0] for category in categories if category[0]]