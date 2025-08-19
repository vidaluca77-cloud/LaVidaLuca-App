"""
User management endpoints for admin operations.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...models.user import User
from ...schemas.auth import UserManagement, AuditLog
from ...schemas.user import UserResponse, UserListResponse
from ...services.user_management_service import UserManagementService
from ..endpoints.auth import get_current_user


router = APIRouter()


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Verify current user is an admin."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


@router.get("/users", response_model=List[UserListResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_verified: Optional[bool] = Query(None),
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of users with optional filtering."""
    user_mgmt_service = UserManagementService(db)
    
    users, total = user_mgmt_service.get_users(
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active,
        is_verified=is_verified
    )
    
    return [
        UserListResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at
        )
        for user in users
    ]


@router.get("/users/{user_id}", response_model=dict)
def get_user_details(
    user_id: str,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get detailed user information including security stats."""
    user_mgmt_service = UserManagementService(db)
    
    user_details = user_mgmt_service.get_user_details(user_id)
    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Convert user model to response format
    user = user_details["user"]
    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "is_locked": user.is_locked,
            "two_factor_enabled": user.two_factor_enabled,
            "failed_login_attempts": user.failed_login_attempts,
            "created_at": user.created_at,
            "last_login": user.last_login
        },
        "active_sessions": user_details["active_sessions"],
        "recent_login_attempts": user_details["recent_login_attempts"],
        "lockout_history": user_details["lockout_history"]
    }


@router.post("/users/{user_id}/manage")
def manage_user(
    user_id: str,
    action_data: UserManagement,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Perform user management action."""
    user_mgmt_service = UserManagementService(db)
    
    # Set the user_id from the path
    action_data.user_id = user_id
    
    try:
        result = user_mgmt_service.manage_user(action_data, str(admin_user.id))
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/security/stats")
def get_security_stats(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get security statistics for admin dashboard."""
    user_mgmt_service = UserManagementService(db)
    return user_mgmt_service.get_security_stats()


@router.get("/security/suspicious-activities")
def get_suspicious_activities(
    limit: int = Query(50, le=100),
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get suspicious activities for security monitoring."""
    user_mgmt_service = UserManagementService(db)
    return {
        "activities": user_mgmt_service.get_suspicious_activities(limit)
    }


@router.post("/security/cleanup")
def cleanup_expired_data(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Manually trigger cleanup of expired sessions and tokens."""
    from ...services.session_service import SessionService
    
    session_service = SessionService(db)
    expired_sessions, expired_tokens = session_service.cleanup_expired_sessions()
    
    return {
        "message": "Cleanup completed",
        "expired_sessions_cleaned": expired_sessions,
        "expired_tokens_cleaned": expired_tokens
    }