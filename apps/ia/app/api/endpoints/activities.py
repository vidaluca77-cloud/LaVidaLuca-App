from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import json

from app.db.database import get_db
from app.auth.jwt_handler import get_current_user_optional, get_current_user
from app.models.models import Activity

router = APIRouter()

# Pydantic models
class ActivityResponse(BaseModel):
    id: str
    slug: str
    title: str
    category: str
    summary: str
    description: Optional[str]
    duration_min: int
    skill_tags: List[str]
    seasonality: List[str]
    safety_level: int
    materials: List[str]
    is_active: bool

    class Config:
        from_attributes = True

class ActivityCreate(BaseModel):
    slug: str
    title: str
    category: str
    summary: str
    description: Optional[str] = None
    duration_min: int
    skill_tags: List[str]
    seasonality: List[str]
    safety_level: int = 1
    materials: List[str] = []

@router.get("/", response_model=List[ActivityResponse])
async def get_activities(
    category: Optional[str] = Query(None, description="Filter by category"),
    skill: Optional[str] = Query(None, description="Filter by skill"),
    season: Optional[str] = Query(None, description="Filter by season"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Get list of activities with optional filters"""
    
    query = db.query(Activity).filter(Activity.is_active == True)
    
    # Apply filters
    if category:
        query = query.filter(Activity.category == category)
    
    if skill:
        # Filter by skill tag (stored as JSON string)
        query = query.filter(Activity.skill_tags.contains(f'"{skill}"'))
    
    if season:
        # Filter by seasonality (stored as JSON string) 
        query = query.filter(Activity.seasonality.contains(f'"{season}"'))
    
    activities = query.offset(skip).limit(limit).all()
    
    # Convert JSON strings back to lists for response
    result = []
    for activity in activities:
        activity_dict = {
            "id": str(activity.id),
            "slug": activity.slug,
            "title": activity.title,
            "category": activity.category,
            "summary": activity.summary,
            "description": activity.description,
            "duration_min": activity.duration_min,
            "skill_tags": json.loads(activity.skill_tags) if activity.skill_tags else [],
            "seasonality": json.loads(activity.seasonality) if activity.seasonality else [],
            "safety_level": activity.safety_level,
            "materials": json.loads(activity.materials) if activity.materials else [],
            "is_active": activity.is_active
        }
        result.append(ActivityResponse(**activity_dict))
    
    return result

@router.get("/{activity_slug}", response_model=ActivityResponse)
async def get_activity(
    activity_slug: str,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Get specific activity by slug"""
    
    activity = db.query(Activity).filter(
        Activity.slug == activity_slug,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activité non trouvée"
        )
    
    # Convert JSON strings back to lists
    return ActivityResponse(
        id=str(activity.id),
        slug=activity.slug,
        title=activity.title,
        category=activity.category,
        summary=activity.summary,
        description=activity.description,
        duration_min=activity.duration_min,
        skill_tags=json.loads(activity.skill_tags) if activity.skill_tags else [],
        seasonality=json.loads(activity.seasonality) if activity.seasonality else [],
        safety_level=activity.safety_level,
        materials=json.loads(activity.materials) if activity.materials else [],
        is_active=activity.is_active
    )

@router.post("/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_data: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new activity (authenticated users only)"""
    
    # Check if activity with same slug exists
    existing_activity = db.query(Activity).filter(Activity.slug == activity_data.slug).first()
    if existing_activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Une activité avec ce slug existe déjà"
        )
    
    # Create new activity
    db_activity = Activity(
        slug=activity_data.slug,
        title=activity_data.title,
        category=activity_data.category,
        summary=activity_data.summary,
        description=activity_data.description,
        duration_min=activity_data.duration_min,
        skill_tags=json.dumps(activity_data.skill_tags),
        seasonality=json.dumps(activity_data.seasonality),
        safety_level=activity_data.safety_level,
        materials=json.dumps(activity_data.materials)
    )
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return ActivityResponse(
        id=str(db_activity.id),
        slug=db_activity.slug,
        title=db_activity.title,
        category=db_activity.category,
        summary=db_activity.summary,
        description=db_activity.description,
        duration_min=db_activity.duration_min,
        skill_tags=json.loads(db_activity.skill_tags),
        seasonality=json.loads(db_activity.seasonality),
        safety_level=db_activity.safety_level,
        materials=json.loads(db_activity.materials),
        is_active=db_activity.is_active
    )