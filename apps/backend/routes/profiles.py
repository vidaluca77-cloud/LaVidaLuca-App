"""
Profile management routes for user profiles.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_

from ..database import get_db_session
from ..models.user import User
from ..models.profile import Profile
from ..schemas.profile import (
    ProfileCreate, ProfileUpdate, ProfileResponse, 
    ProfileListResponse, ProfileSearchFilters
)
from ..schemas.common import ApiResponse, PaginationParams, PaginatedResponse
from ..auth.dependencies import get_current_active_user


router = APIRouter()


@router.post("/", response_model=ApiResponse[ProfileResponse])
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new profile for the current user.
    """
    # Check if user already has a profile
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    existing_profile = result.scalar_one_or_none()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a profile. Use PUT to update."
        )
    
    # Create new profile
    new_profile = Profile(
        user_id=current_user.id,
        **profile_data.dict()
    )
    
    # Mark as complete if enough data is provided
    if profile_data.skills and profile_data.location and profile_data.interests:
        new_profile.is_complete = True
    
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    
    return ApiResponse(
        success=True,
        data=ProfileResponse.from_orm(new_profile),
        message="Profile created successfully"
    )


@router.get("/", response_model=ApiResponse[PaginatedResponse[ProfileListResponse]])
async def list_profiles(
    pagination: PaginationParams = Depends(),
    filters: ProfileSearchFilters = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    List public profiles with optional filtering and pagination.
    """
    # Build query with filters - only show public profiles
    query = select(Profile).where(Profile.is_public == True)
    
    if filters.skills:
        for skill in filters.skills:
            query = query.where(Profile.skills.contains([skill]))
    
    if filters.location:
        query = query.where(Profile.location.ilike(f"%{filters.location}%"))
    
    if filters.experience_level:
        query = query.where(Profile.experience_level == filters.experience_level)
    
    if filters.interests:
        for interest in filters.interests:
            query = query.where(Profile.interests.contains([interest]))
    
    if filters.mentoring_interest is not None:
        query = query.where(Profile.mentoring_interest == filters.mentoring_interest)
    
    if filters.collaboration_preference:
        query = query.where(Profile.collaboration_preference == filters.collaboration_preference)
    
    if filters.travel_willingness:
        query = query.where(Profile.travel_willingness == filters.travel_willingness)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    # Get profiles with pagination
    profiles_result = await db.execute(
        query
        .offset(pagination.offset)
        .limit(pagination.size)
        .order_by(Profile.updated_at.desc())
    )
    profiles = profiles_result.scalars().all()
    
    # Filter by completion percentage if specified
    if filters.min_completion:
        profiles = [p for p in profiles if p.completion_percentage >= filters.min_completion]
    
    profile_responses = [ProfileListResponse.from_orm(profile) for profile in profiles]
    paginated_data = PaginatedResponse.create(profile_responses, total, pagination)
    
    return ApiResponse(
        success=True,
        data=paginated_data,
        message="Profiles retrieved successfully"
    )


@router.get("/me", response_model=ApiResponse[ProfileResponse])
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get the current user's profile.
    """
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Create one first."
        )
    
    return ApiResponse(
        success=True,
        data=ProfileResponse.from_orm(profile),
        message="Profile retrieved successfully"
    )


@router.get("/{profile_id}", response_model=ApiResponse[ProfileResponse])
async def get_profile(
    profile_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a profile by ID (only if public).
    """
    result = await db.execute(
        select(Profile).where(
            and_(Profile.id == profile_id, Profile.is_public == True)
        )
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found or not public"
        )
    
    return ApiResponse(
        success=True,
        data=ProfileResponse.from_orm(profile),
        message="Profile retrieved successfully"
    )


@router.put("/me", response_model=ApiResponse[ProfileResponse])
async def update_my_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update the current user's profile.
    """
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Create one first."
        )
    
    # Update profile fields
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    # Check if profile should be marked as complete
    if (profile.skills and profile.location and profile.interests and 
        profile.experience_level != "beginner"):
        profile.is_complete = True
    
    await db.commit()
    await db.refresh(profile)
    
    return ApiResponse(
        success=True,
        data=ProfileResponse.from_orm(profile),
        message="Profile updated successfully"
    )


@router.delete("/me", response_model=ApiResponse[dict])
async def delete_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete the current user's profile.
    """
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    await db.delete(profile)
    await db.commit()
    
    return ApiResponse(
        success=True,
        data={"deleted_profile_id": str(profile.id)},
        message="Profile deleted successfully"
    )


@router.get("/search/skills", response_model=ApiResponse[list[str]])
async def get_available_skills(
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get list of all skills used in profiles.
    """
    result = await db.execute(
        select(Profile.skills).where(Profile.is_public == True)
    )
    all_skills = result.scalars().all()
    
    # Flatten and deduplicate skills
    unique_skills = set()
    for skills_list in all_skills:
        if skills_list:
            unique_skills.update(skills_list)
    
    return ApiResponse(
        success=True,
        data=sorted(list(unique_skills)),
        message="Available skills retrieved successfully"
    )


@router.get("/search/interests", response_model=ApiResponse[list[str]])
async def get_available_interests(
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get list of all interests used in profiles.
    """
    result = await db.execute(
        select(Profile.interests).where(Profile.is_public == True)
    )
    all_interests = result.scalars().all()
    
    # Flatten and deduplicate interests
    unique_interests = set()
    for interests_list in all_interests:
        if interests_list:
            unique_interests.update(interests_list)
    
    return ApiResponse(
        success=True,
        data=sorted(list(unique_interests)),
        message="Available interests retrieved successfully"
    )