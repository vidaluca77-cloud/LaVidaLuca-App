"""
Activities router for managing activities.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

from database.database import get_db
from database.models import Activity, User
from schemas.schemas import (
    ActivityCreate, ActivityUpdate, ActivityResponse, ActivityFilter,
    PaginationParams, PaginatedResponse, ApiResponse, ActivityCategory
)
from auth.auth import get_current_active_user
from monitoring.logger import context_logger

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def get_activities(
    # Pagination
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    
    # Filters
    category: Optional[ActivityCategory] = None,
    skill_tags: Optional[List[str]] = Query(None),
    duration_min_min: Optional[int] = Query(None, ge=1),
    duration_min_max: Optional[int] = Query(None, ge=1),
    safety_level_max: Optional[int] = Query(None, ge=1, le=5),
    location_type: Optional[str] = None,
    season: Optional[List[str]] = Query(None),
    search: Optional[str] = None,
    
    db: AsyncSession = Depends(get_db)
):
    """
    Get paginated list of activities with optional filters.
    
    Args:
        page: Page number
        size: Page size
        category: Activity category filter
        skill_tags: Skill tags filter
        duration_min_min: Minimum duration filter
        duration_min_max: Maximum duration filter
        safety_level_max: Maximum safety level filter
        location_type: Location type filter
        season: Season filter
        search: Text search in title and summary
        db: Database session
        
    Returns:
        PaginatedResponse: Paginated activities
    """
    # Build base query
    query = select(Activity)
    
    # Apply filters
    conditions = []
    
    if category:
        conditions.append(Activity.category == category)
    
    if skill_tags:
        # Activities that have any of the specified skills
        for skill in skill_tags:
            conditions.append(func.json_extract(Activity.skill_tags, f'$[*]').like(f'%{skill}%'))
    
    if duration_min_min:
        conditions.append(Activity.duration_min >= duration_min_min)
    
    if duration_min_max:
        conditions.append(Activity.duration_min <= duration_min_max)
    
    if safety_level_max:
        conditions.append(Activity.safety_level <= safety_level_max)
    
    if location_type:
        conditions.append(Activity.location_type == location_type)
    
    if season:
        # Activities available in any of the specified seasons
        for s in season:
            conditions.append(func.json_extract(Activity.season, f'$[*]').like(f'%{s}%'))
    
    if search:
        search_term = f"%{search}%"
        conditions.append(
            or_(
                Activity.title.ilike(search_term),
                Activity.summary.ilike(search_term),
                Activity.description.ilike(search_term)
            )
        )
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination and get results
    query = query.offset((page - 1) * size).limit(size).order_by(Activity.created_at.desc())
    result = await db.execute(query)
    activities = result.scalars().all()
    
    # Calculate pagination info
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[ActivityResponse.model_validate(activity) for activity in activities],
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific activity by ID.
    
    Args:
        activity_id: Activity ID
        db: Database session
        
    Returns:
        ActivityResponse: Activity data
    """
    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return ActivityResponse.model_validate(activity)


@router.post("/", response_model=ApiResponse)
async def create_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new activity.
    
    Args:
        activity_data: Activity creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ApiResponse: Creation result
    """
    db_activity = Activity(
        title=activity_data.title,
        category=activity_data.category,
        summary=activity_data.summary,
        description=activity_data.description,
        duration_min=activity_data.duration_min,
        skill_tags=activity_data.skill_tags,
        safety_level=activity_data.safety_level,
        materials=activity_data.materials,
        location_type=activity_data.location_type,
        season=activity_data.season,
        created_by=current_user.id
    )
    
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    
    context_logger.info(
        "Activity created successfully",
        activity_id=db_activity.id,
        user_id=current_user.id,
        title=activity_data.title
    )
    
    return ApiResponse(
        success=True,
        data={"activity_id": db_activity.id},
        message="Activity created successfully"
    )


@router.put("/{activity_id}", response_model=ApiResponse)
async def update_activity(
    activity_id: str,
    activity_data: ActivityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing activity.
    
    Args:
        activity_id: Activity ID
        activity_data: Activity update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ApiResponse: Update result
    """
    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user can edit (creator or admin logic can be added here)
    if activity.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this activity"
        )
    
    # Update fields
    update_data = activity_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    await db.commit()
    await db.refresh(activity)
    
    context_logger.info(
        "Activity updated successfully",
        activity_id=activity_id,
        user_id=current_user.id
    )
    
    return ApiResponse(
        success=True,
        data={"activity_id": activity_id},
        message="Activity updated successfully"
    )


@router.delete("/{activity_id}", response_model=ApiResponse)
async def delete_activity(
    activity_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an activity.
    
    Args:
        activity_id: Activity ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ApiResponse: Deletion result
    """
    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user can delete (creator or admin logic can be added here)
    if activity.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this activity"
        )
    
    await db.delete(activity)
    await db.commit()
    
    context_logger.info(
        "Activity deleted successfully",
        activity_id=activity_id,
        user_id=current_user.id
    )
    
    return ApiResponse(
        success=True,
        message="Activity deleted successfully"
    )


@router.get("/categories/list", response_model=List[str])
async def get_activity_categories():
    """
    Get list of available activity categories.
    
    Returns:
        List[str]: Available categories
    """
    return [category.value for category in ActivityCategory]