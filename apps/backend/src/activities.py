from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

try:
    from .database import get_db
    from .models import Activity, User
    from .schemas import ActivityCreate, ActivityResponse
    from .auth.router import get_current_user
except ImportError:
    from database import get_db
    from models import Activity, User
    from schemas import ActivityCreate, ActivityResponse
    from auth.router import get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("/", response_model=ActivityResponse)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_activity = Activity(**activity.model_dump(), user_id=current_user.id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@router.get("/", response_model=List[ActivityResponse])
def get_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    activities = db.query(Activity).filter(Activity.user_id == current_user.id).offset(skip).limit(limit).all()
    return activities


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = db.query(Activity).filter(Activity.id == activity_id, Activity.user_id == current_user.id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity