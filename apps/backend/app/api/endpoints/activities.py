from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload

from ...core.database import get_db
from ...core.security import get_current_user, get_current_user_id
from ...models import User, Activity, ActivitySuggestion
from ...schemas import (
    Activity as ActivitySchema, ActivityCreate, ActivityUpdate, 
    ActivitySummary, ActivitySearchFilters
)
from ...services.matching import MatchingService


router = APIRouter()
matching_service = MatchingService()


@router.get("/", response_model=List[ActivitySummary])
async def get_activities(
    db: AsyncSession = Depends(get_db),
    category: Optional[str] = Query(None),
    difficulty_level: Optional[str] = Query(None),
    location_type: Optional[str] = Query(None),
    is_featured: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get activities with filtering and pagination."""
    query = select(Activity).where(
        and_(Activity.is_published == True, Activity.approval_status == "approved")
    )
    
    # Apply filters
    if category:
        query = query.where(Activity.category == category)
    
    if difficulty_level:
        query = query.where(Activity.difficulty_level == difficulty_level)
    
    if location_type:
        query = query.where(Activity.location_type == location_type)
        
    if is_featured is not None:
        query = query.where(Activity.is_featured == is_featured)
    
    if search:
        search_filter = or_(
            Activity.title.icontains(search),
            Activity.description.icontains(search),
            Activity.short_description.icontains(search)
        )
        query = query.where(search_filter)
    
    # Apply ordering (featured first, then by creation date)
    query = query.order_by(desc(Activity.is_featured), desc(Activity.created_at))
    
    # Apply pagination
    query = query.offset(offset).limit(limit)
    
    result = await db.execute(query)
    activities = result.scalars().all()
    
    return activities


@router.get("/featured", response_model=List[ActivitySummary])
async def get_featured_activities(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(6, ge=1, le=20)
):
    """Get featured activities."""
    query = select(Activity).where(
        and_(
            Activity.is_published == True,
            Activity.approval_status == "approved",
            Activity.is_featured == True
        )
    ).order_by(desc(Activity.created_at)).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/categories")
async def get_activity_categories(db: AsyncSession = Depends(get_db)):
    """Get available activity categories."""
    result = await db.execute(
        select(Activity.category, func.count(Activity.id).label('count'))
        .where(and_(Activity.is_published == True, Activity.approval_status == "approved"))
        .group_by(Activity.category)
        .order_by(desc('count'))
    )
    
    categories = [{"name": row[0], "count": row[1]} for row in result.all()]
    return {"categories": categories}


@router.get("/{activity_id}", response_model=ActivitySchema)
async def get_activity(
    activity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: Optional[str] = Depends(get_current_user_id)
):
    """Get a specific activity by ID."""
    result = await db.execute(
        select(Activity)
        .options(selectinload(Activity.creator))
        .where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if activity is published or user is the creator
    if not activity.is_published and activity.creator_id != current_user_id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Increment view count if user is authenticated and not the creator
    if current_user_id and current_user_id != activity.creator_id:
        activity.view_count += 1
        await db.commit()
    
    return activity


@router.post("/", response_model=ActivitySchema)
async def create_activity(
    activity: ActivityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new activity."""
    db_activity = Activity(
        **activity.dict(),
        creator_id=current_user.id
    )
    
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    
    return db_activity


@router.put("/{activity_id}", response_model=ActivitySchema)
async def update_activity(
    activity_id: str,
    activity_update: ActivityUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an activity."""
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user is the creator or admin
    if activity.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to update this activity")
    
    # Update fields
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    await db.commit()
    await db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an activity."""
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user is the creator or admin
    if activity.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to delete this activity")
    
    await db.delete(activity)
    await db.commit()
    
    return {"message": "Activity deleted successfully"}


@router.get("/{activity_id}/similar", response_model=List[ActivitySummary])
async def get_similar_activities(
    activity_id: str,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(5, ge=1, le=10)
):
    """Get activities similar to the specified activity."""
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    similar_activities = await matching_service.find_similar_activities(
        activity, db, limit
    )
    
    return similar_activities


@router.post("/{activity_id}/publish", response_model=ActivitySchema)
async def publish_activity(
    activity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Publish an activity (for creators and admins)."""
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check permissions
    if activity.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to publish this activity")
    
    activity.is_published = True
    activity.published_at = func.now()
    
    # Auto-approve if user is admin or teacher
    if current_user.is_superuser or current_user.role in ["teacher", "coordinator"]:
        activity.approval_status = "approved"
    else:
        activity.approval_status = "pending"
    
    await db.commit()
    await db.refresh(activity)
    
    return activity


@router.get("/my/activities", response_model=List[ActivitySchema])
async def get_my_activities(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    include_unpublished: bool = Query(True)
):
    """Get activities created by the current user."""
    query = select(Activity).where(Activity.creator_id == current_user.id)
    
    if not include_unpublished:
        query = query.where(Activity.is_published == True)
    
    query = query.order_by(desc(Activity.created_at))
    
    result = await db.execute(query)
    return result.scalars().all()