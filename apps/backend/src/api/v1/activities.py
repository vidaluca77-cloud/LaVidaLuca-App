"""Activity API routes."""

from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...api.deps import get_current_active_user, get_current_instructor_or_admin
from ...db.session import get_db
from ...models.activity import Activity, ActivityCategory
from ...models.user import User
from ...schemas.activity import (
    Activity as ActivitySchema,
    ActivityCreate,
    ActivitySummary,
    ActivityUpdate,
    ActivityWithLocation
)

router = APIRouter()


@router.get("/", response_model=List[ActivityWithLocation])
def read_activities(
    skip: int = 0,
    limit: int = 100,
    category: Optional[ActivityCategory] = Query(None),
    location_id: Optional[UUID] = Query(None),
    difficulty_level: Optional[int] = Query(None, ge=1, le=5),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Retrieve activities with filters."""
    query = db.query(Activity).filter(Activity.is_active == True)
    
    if category:
        query = query.filter(Activity.category == category)
    if location_id:
        query = query.filter(Activity.location_id == location_id)
    if difficulty_level:
        query = query.filter(Activity.difficulty_level == difficulty_level)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.post("/", response_model=ActivitySchema)
def create_activity(
    activity_in: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Create new activity."""
    # Check if slug already exists
    existing_activity = db.query(Activity).filter(Activity.slug == activity_in.slug).first()
    if existing_activity:
        raise HTTPException(
            status_code=400,
            detail="Activity with this slug already exists"
        )
    
    db_activity = Activity(**activity_in.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity


@router.get("/{activity_id}", response_model=ActivityWithLocation)
def read_activity(
    activity_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.get("/slug/{slug}", response_model=ActivityWithLocation)
def read_activity_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get activity by slug."""
    activity = db.query(Activity).filter(Activity.slug == slug).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.put("/{activity_id}", response_model=ActivitySchema)
def update_activity(
    activity_id: UUID,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Update activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity_data = activity_update.dict(exclude_unset=True)
    for field, value in activity_data.items():
        setattr(activity, field, value)
    
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.delete("/{activity_id}")
def delete_activity(
    activity_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Delete activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Soft delete - just mark as inactive
    activity.is_active = False
    db.add(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}


@router.get("/categories/", response_model=List[str])
def get_activity_categories() -> Any:
    """Get all activity categories."""
    return [category.value for category in ActivityCategory]


@router.get("/search/", response_model=List[ActivitySummary])
def search_activities(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Search activities by title, description, or skill tags."""
    activities = (
        db.query(Activity)
        .filter(
            Activity.is_active == True,
            Activity.title.ilike(f"%{q}%")
            | Activity.description.ilike(f"%{q}%")
            | Activity.skill_tags.any(q)
        )
        .all()
    )
    return activities