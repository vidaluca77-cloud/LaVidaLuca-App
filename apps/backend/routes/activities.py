"""
Activity management routes for educational activities and learning experiences.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_

from ..database import get_db_session
from ..models.user import User
from ..models.activity import Activity
from ..schemas.activity import (
    ActivityCreate, ActivityUpdate, ActivityResponse, 
    ActivityListResponse, ActivitySearchFilters
)
from ..schemas.common import ApiResponse, PaginationParams, PaginatedResponse
from ..auth.dependencies import get_current_active_user


router = APIRouter()


@router.post("/", response_model=ApiResponse[ActivityResponse])
async def create_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new educational activity.
    """
    new_activity = Activity(
        **activity_data.dict(),
        created_by=current_user.id
    )
    
    db.add(new_activity)
    await db.commit()
    await db.refresh(new_activity)
    
    return ApiResponse(
        success=True,
        data=ActivityResponse.from_orm(new_activity),
        message="Activity created successfully"
    )


@router.get("/", response_model=ApiResponse[PaginatedResponse[ActivityListResponse]])
async def list_activities(
    pagination: PaginationParams = Depends(),
    filters: ActivitySearchFilters = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    List activities with optional filtering and pagination.
    """
    # Build query with filters
    query = select(Activity).where(Activity.is_published == True)
    
    if filters.category:
        query = query.where(Activity.category == filters.category)
    
    if filters.min_duration:
        query = query.where(Activity.duration_min >= filters.min_duration)
    
    if filters.max_duration:
        query = query.where(Activity.duration_min <= filters.max_duration)
    
    if filters.difficulty_level:
        query = query.where(Activity.difficulty_level == filters.difficulty_level)
    
    if filters.safety_level:
        query = query.where(Activity.safety_level <= filters.safety_level)
    
    if filters.location_type:
        query = query.where(Activity.location_type == filters.location_type)
    
    if filters.is_featured is not None:
        query = query.where(Activity.is_featured == filters.is_featured)
    
    if filters.skill_tags:
        for tag in filters.skill_tags:
            query = query.where(Activity.skill_tags.contains([tag]))
    
    if filters.season_tags:
        for tag in filters.season_tags:
            query = query.where(Activity.season_tags.contains([tag]))
    
    if filters.keywords:
        search_term = f"%{filters.keywords.lower()}%"
        query = query.where(
            or_(
                Activity.title.ilike(search_term),
                Activity.summary.ilike(search_term),
                Activity.description.ilike(search_term)
            )
        )
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    # Get activities with pagination
    activities_result = await db.execute(
        query
        .offset(pagination.offset)
        .limit(pagination.size)
        .order_by(Activity.is_featured.desc(), Activity.created_at.desc())
    )
    activities = activities_result.scalars().all()
    
    activity_responses = [ActivityListResponse.from_orm(activity) for activity in activities]
    paginated_data = PaginatedResponse.create(activity_responses, total, pagination)
    
    return ApiResponse(
        success=True,
        data=paginated_data,
        message="Activities retrieved successfully"
    )


@router.get("/{activity_id}", response_model=ApiResponse[ActivityResponse])
async def get_activity(
    activity_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get activity by ID.
    """
    result = await db.execute(
        select(Activity).where(
            and_(Activity.id == activity_id, Activity.is_published == True)
        )
    )
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return ApiResponse(
        success=True,
        data=ActivityResponse.from_orm(activity),
        message="Activity retrieved successfully"
    )


@router.put("/{activity_id}", response_model=ApiResponse[ActivityResponse])
async def update_activity(
    activity_id: str,
    activity_update: ActivityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update an existing activity.
    """
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user can edit this activity (owner or admin)
    if activity.created_by != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this activity"
        )
    
    # Update activity fields
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    await db.commit()
    await db.refresh(activity)
    
    return ApiResponse(
        success=True,
        data=ActivityResponse.from_orm(activity),
        message="Activity updated successfully"
    )


@router.delete("/{activity_id}", response_model=ApiResponse[dict])
async def delete_activity(
    activity_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete an activity.
    """
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user can delete this activity (owner or admin)
    if activity.created_by != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this activity"
        )
    
    await db.delete(activity)
    await db.commit()
    
    return ApiResponse(
        success=True,
        data={"deleted_activity_id": activity_id},
        message="Activity deleted successfully"
    )