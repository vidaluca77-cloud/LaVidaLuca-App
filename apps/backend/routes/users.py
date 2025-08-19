"""
User management routes for profile and user operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..database import get_db_session
from ..models.user import User
from ..schemas.user import UserUpdate, UserResponse, UserListResponse
from ..schemas.common import ApiResponse, PaginationParams, PaginatedResponse
from ..auth.dependencies import get_current_active_user, require_admin


router = APIRouter()


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's profile information.
    """
    return ApiResponse(
        success=True,
        data=UserResponse.model_validate(current_user),
        message="User profile retrieved successfully"
    )


@router.put("/me", response_model=ApiResponse[UserResponse])
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update current user's profile information.
    """
    # Update user fields
    if user_update.first_name is not None:
        current_user.first_name = user_update.first_name
    if user_update.last_name is not None:
        current_user.last_name = user_update.last_name
    if user_update.profile is not None:
        current_user.profile = user_update.profile
    
    await db.commit()
    await db.refresh(current_user)
    
    return ApiResponse(
        success=True,
        data=UserResponse.model_validate(current_user),
        message="Profile updated successfully"
    )


@router.get("/{user_id}", response_model=ApiResponse[UserResponse])
async def get_user_by_id(
    user_id: str,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get user by ID (public profile info only).
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return ApiResponse(
        success=True,
        data=UserResponse.model_validate(user),
        message="User retrieved successfully"
    )


@router.get("/", response_model=ApiResponse[PaginatedResponse[UserListResponse]])
async def list_users(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db_session),
    admin_user: User = Depends(require_admin)
):
    """
    List all users (admin only).
    """
    # Get total count
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar()
    
    # Get users with pagination
    result = await db.execute(
        select(User)
        .offset(pagination.offset)
        .limit(pagination.size)
        .order_by(User.created_at.desc())
    )
    users = result.scalars().all()
    
    user_responses = [UserListResponse.model_validate(user) for user in users]
    paginated_data = PaginatedResponse.create(user_responses, total, pagination)
    
    return ApiResponse(
        success=True,
        data=paginated_data,
        message="Users retrieved successfully"
    )


@router.delete("/{user_id}", response_model=ApiResponse[dict])
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db_session),
    admin_user: User = Depends(require_admin)
):
    """
    Delete user by ID (admin only).
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await db.delete(user)
    await db.commit()
    
    return ApiResponse(
        success=True,
        data={"deleted_user_id": user_id},
        message="User deleted successfully"
    )