"""
Users router for managing user profiles and interactions.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from database.database import get_db
from database.models import User, UserActivity, Activity
from schemas.schemas import (
    UserUpdate, UserResponse, UserActivityCreate, UserActivityResponse,
    PaginationParams, PaginatedResponse, ApiResponse
)
from auth.auth import get_current_active_user
from monitoring.logger import context_logger

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's profile.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: User profile data
    """
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=ApiResponse)
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user's profile.
    
    Args:
        user_data: User update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ApiResponse: Update result
    """
    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    context_logger.info(
        "User profile updated successfully",
        user_id=current_user.id
    )
    
    return ApiResponse(
        success=True,
        data={"user_id": current_user.id},
        message="Profile updated successfully"
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a user's public profile.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        UserResponse: User profile data
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)


@router.post("/activities", response_model=ApiResponse)
async def add_user_activity(
    activity_data: UserActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add an activity interaction for the current user.
    
    Args:
        activity_data: User activity data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ApiResponse: Creation result
    """
    # Check if activity exists
    result = await db.execute(
        select(Activity).where(Activity.id == activity_data.activity_id)
    )
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if interaction already exists
    existing_result = await db.execute(
        select(UserActivity).where(
            and_(
                UserActivity.user_id == current_user.id,
                UserActivity.activity_id == activity_data.activity_id,
                UserActivity.interaction_type == activity_data.interaction_type
            )
        )
    )
    existing_interaction = existing_result.scalar_one_or_none()
    
    if existing_interaction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interaction already exists"
        )
    
    # Create new user activity
    db_user_activity = UserActivity(
        user_id=current_user.id,
        activity_id=activity_data.activity_id,
        interaction_type=activity_data.interaction_type,
        rating=activity_data.rating,
        notes=activity_data.notes
    )
    
    # Set completion date if it's a completion
    if activity_data.interaction_type == "completed":
        from datetime import datetime
        db_user_activity.completed_at = datetime.utcnow()
    
    db.add(db_user_activity)
    await db.commit()
    await db.refresh(db_user_activity)
    
    context_logger.info(
        "User activity added successfully",
        user_id=current_user.id,
        activity_id=activity_data.activity_id,
        interaction_type=activity_data.interaction_type
    )
    
    return ApiResponse(
        success=True,
        data={"user_activity_id": db_user_activity.id},
        message="Activity interaction added successfully"
    )


@router.get("/activities/me", response_model=PaginatedResponse)
async def get_current_user_activities(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    interaction_type: str = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's activity interactions.
    
    Args:
        page: Page number
        size: Page size
        interaction_type: Filter by interaction type
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        PaginatedResponse: Paginated user activities
    """
    # Build query
    query = select(UserActivity).where(UserActivity.user_id == current_user.id)
    
    if interaction_type:
        query = query.where(UserActivity.interaction_type == interaction_type)
    
    # Get total count
    from sqlalchemy import func
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination and get results
    query = query.offset((page - 1) * size).limit(size).order_by(UserActivity.created_at.desc())
    result = await db.execute(query)
    user_activities = result.scalars().all()
    
    # Calculate pagination info
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[UserActivityResponse.model_validate(ua) for ua in user_activities],
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.delete("/activities/{user_activity_id}", response_model=ApiResponse)
async def remove_user_activity(
    user_activity_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a user activity interaction.
    
    Args:
        user_activity_id: User activity ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ApiResponse: Deletion result
    """
    result = await db.execute(
        select(UserActivity).where(
            and_(
                UserActivity.id == user_activity_id,
                UserActivity.user_id == current_user.id
            )
        )
    )
    user_activity = result.scalar_one_or_none()
    
    if not user_activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User activity not found"
        )
    
    await db.delete(user_activity)
    await db.commit()
    
    context_logger.info(
        "User activity removed successfully",
        user_id=current_user.id,
        user_activity_id=user_activity_id
    )
    
    return ApiResponse(
        success=True,
        message="Activity interaction removed successfully"
    )


@router.get("/activities/{user_id}", response_model=List[UserActivityResponse])
async def get_user_public_activities(
    user_id: str,
    interaction_type: str = Query("completed"),  # Default to completed activities
    db: AsyncSession = Depends(get_db)
):
    """
    Get a user's public activity interactions.
    
    Args:
        user_id: User ID
        interaction_type: Filter by interaction type
        db: Database session
        
    Returns:
        List[UserActivityResponse]: User's public activities
    """
    # Check if user exists and is active
    user_result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = user_result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user activities (only public ones - completed activities)
    query = select(UserActivity).where(
        and_(
            UserActivity.user_id == user_id,
            UserActivity.interaction_type == interaction_type
        )
    ).order_by(UserActivity.created_at.desc()).limit(50)  # Limit for public view
    
    result = await db.execute(query)
    user_activities = result.scalars().all()
    
    return [UserActivityResponse.model_validate(ua) for ua in user_activities]