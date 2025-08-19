"""
Example usage of enhanced authentication features.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db_session
from ..models.user import User, UserRole
from ..auth.dependencies import (
    get_current_active_user,
    require_admin,
    require_moderator,
    require_permission,
    require_role
)
from ..schemas.common import ApiResponse


router = APIRouter()


@router.get("/profile", response_model=ApiResponse[dict])
async def get_my_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's profile (requires authentication).
    """
    return ApiResponse(
        success=True,
        data=current_user.to_dict(),
        message="User profile retrieved"
    )


@router.get("/admin-only", response_model=ApiResponse[dict])
async def admin_only_endpoint(
    current_user: User = Depends(require_admin)
):
    """
    Example endpoint that requires admin privileges.
    """
    return ApiResponse(
        success=True,
        data={"message": "This is an admin-only endpoint", "user": current_user.email},
        message="Admin access granted"
    )


@router.get("/moderator-area", response_model=ApiResponse[dict])
async def moderator_area(
    current_user: User = Depends(require_moderator)
):
    """
    Example endpoint that requires moderator privileges or higher.
    """
    return ApiResponse(
        success=True,
        data={
            "message": "Welcome to moderator area",
            "user": current_user.email,
            "role": current_user.role.value
        },
        message="Moderator access granted"
    )


@router.get("/manage-users", response_model=ApiResponse[dict])
async def manage_users_endpoint(
    current_user: User = Depends(require_permission("manage_users"))
):
    """
    Example endpoint that requires specific permission.
    """
    return ApiResponse(
        success=True,
        data={
            "message": "User management interface",
            "permissions": ["manage_users"],
            "user": current_user.email
        },
        message="User management access granted"
    )


@router.post("/promote-user", response_model=ApiResponse[dict])
async def promote_user(
    user_email: str,
    new_role: UserRole,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Example endpoint to promote user role (requires admin).
    """
    from sqlalchemy import select
    
    # Find user to promote
    result = await db.execute(select(User).where(User.email == user_email))
    user_to_promote = result.scalar_one_or_none()
    
    if not user_to_promote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Only superusers can promote to superuser
    if new_role == UserRole.SUPERUSER and current_user.role != UserRole.SUPERUSER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can promote to superuser role"
        )
    
    # Update user role
    old_role = user_to_promote.role
    user_to_promote.role = new_role
    await db.commit()
    
    return ApiResponse(
        success=True,
        data={
            "user_email": user_email,
            "old_role": old_role.value,
            "new_role": new_role.value,
            "promoted_by": current_user.email
        },
        message=f"User promoted from {old_role.value} to {new_role.value}"
    )


@router.get("/user-sessions", response_model=ApiResponse[list])
async def get_user_sessions(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get current user's active sessions.
    """
    from ..auth.sessions import session_manager
    
    sessions = await session_manager.get_user_sessions(db, str(current_user.id))
    
    # Remove sensitive data
    safe_sessions = []
    for session in sessions:
        safe_sessions.append({
            "session_id": session.get("session_id"),
            "created_at": session.get("created_at"),
            "last_activity": session.get("last_activity"),
            "user_agent": session.get("user_agent", "Unknown"),
            "ip_address": session.get("ip_address", "Unknown")
        })
    
    return ApiResponse(
        success=True,
        data=safe_sessions,
        message="Active sessions retrieved"
    )


@router.delete("/revoke-session/{session_id}", response_model=ApiResponse[dict])
async def revoke_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Revoke a specific session.
    """
    from ..auth.sessions import session_manager
    
    success = await session_manager.invalidate_session(db, session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return ApiResponse(
        success=True,
        data={"session_id": session_id},
        message="Session revoked successfully"
    )