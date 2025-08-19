from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from database.models import Activity, User
from schemas.activity import Activity as ActivitySchema, ActivityCreate, ActivityUpdate
from auth.security import get_current_active_user

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("/", response_model=ActivitySchema)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if activity with slug already exists
    db_activity = db.query(Activity).filter(Activity.slug == activity.slug).first()
    if db_activity:
        raise HTTPException(status_code=400, detail="Activity with this slug already exists")
    
    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@router.get("/", response_model=List[ActivitySchema])
def read_activities(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    query = db.query(Activity)
    
    if category:
        query = query.filter(Activity.category == category)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/{activity_id}", response_model=ActivitySchema)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.get("/slug/{slug}", response_model=ActivitySchema)
def read_activity_by_slug(slug: str, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.slug == slug).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.put("/{activity_id}", response_model=ActivitySchema)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity_data = activity_update.dict(exclude_unset=True)
    for field, value in activity_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    return activity


@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}


@router.get("/categories/list")
def get_categories(db: Session = Depends(get_db)):
    """Get list of all activity categories with counts"""
    from sqlalchemy import func
    categories = db.query(Activity.category, func.count(Activity.id).label('count')).group_by(Activity.category).all()
    
    category_names = {
        'agri': 'Agriculture',
        'transfo': 'Transformation',
        'artisanat': 'Artisanat',
        'nature': 'Nature',
        'social': 'Social'
    }
    
    result = []
    for cat, count in categories:
        result.append({
            'id': cat,
            'name': category_names.get(cat, cat.title()),
            'count': count
        })
    
    return result