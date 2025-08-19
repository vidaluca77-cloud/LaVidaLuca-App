from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.activity import Activity, ActivityCategory
from app.schemas.activity import Activity as ActivitySchema, ActivityCreate, ActivityUpdate

router = APIRouter()


@router.get("/", response_model=List[ActivitySchema])
async def list_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[ActivityCategory] = None,
    featured: Optional[bool] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all activities with filtering"""
    query = select(Activity).where(Activity.is_active == True)
    
    if category:
        query = query.where(Activity.category == category)
    
    if featured is not None:
        query = query.where(Activity.is_featured == featured)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            Activity.title.ilike(search_term) |
            Activity.summary.ilike(search_term) |
            Activity.description.ilike(search_term)
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    activities = result.scalars().all()
    
    return activities


@router.get("/categories")
async def list_categories():
    """List all activity categories"""
    return [
        {
            "id": "agri",
            "name": "Agriculture",
            "description": "Élevage, cultures, soins aux animaux"
        },
        {
            "id": "transfo",
            "name": "Transformation",
            "description": "Fromage, conserves, pain..."
        },
        {
            "id": "artisanat",
            "name": "Artisanat",
            "description": "Menuiserie, construction, réparation"
        },
        {
            "id": "nature",
            "name": "Environnement",
            "description": "Plantation, compostage, écologie"
        },
        {
            "id": "social",
            "name": "Animation",
            "description": "Accueil, visites, ateliers enfants"
        }
    ]


@router.get("/{activity_id}", response_model=ActivitySchema)
async def get_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific activity by ID"""
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity


@router.get("/slug/{slug}", response_model=ActivitySchema)
async def get_activity_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific activity by slug"""
    result = await db.execute(select(Activity).where(Activity.slug == slug))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity


@router.post("/", response_model=ActivitySchema)
async def create_activity(
    activity: ActivityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new activity (admin only)"""
    # TODO: Add admin role check
    
    # Check if slug already exists
    result = await db.execute(select(Activity).where(Activity.slug == activity.slug))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Activity slug already exists")
    
    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    
    return db_activity


@router.put("/{activity_id}", response_model=ActivitySchema)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an activity (admin only)"""
    # TODO: Add admin role check
    
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Update activity fields
    for field, value in activity_update.dict(exclude_unset=True).items():
        setattr(activity, field, value)
    
    await db.commit()
    await db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Soft delete an activity (admin only)"""
    # TODO: Add admin role check
    
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity.is_active = False
    await db.commit()
    
    return {"message": "Activity deleted successfully"}