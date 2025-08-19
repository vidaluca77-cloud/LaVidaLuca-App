"""
Authentication dependencies for FastAPI endpoints.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..database import get_db_session
from ..models.user import User
from .jwt import jwt_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db_session)
) -> User:
    """
    Get the current authenticated user.
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        Current user from database
        
    Raises:
        HTTPException: If user not found or inactive
    """
    token_data = jwt_handler.verify_access_token(credentials.credentials)
    
    # Fetch user from database
    result = await db.execute(select(User).where(User.id == token_data.user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: Current user from token
        
    Returns:
        Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return current_user


async def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Require the current user to be an admin/superuser.
    
    Args:
        current_user: Current active user
        
    Returns:
        Current user if admin
        
    Raises:
        HTTPException: If user is not an admin
    """
    from ..models.user import UserRole
    
    if not current_user.has_role(UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user


async def require_moderator(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Require the current user to be a moderator or higher.
    
    Args:
        current_user: Current active user
        
    Returns:
        Current user if moderator or higher
        
    Raises:
        HTTPException: If user is not a moderator
    """
    from ..models.user import UserRole
    
    if not current_user.has_role(UserRole.MODERATOR):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator privileges required"
        )
    
    return current_user


def require_permission(permission: str):
    """
    Create a dependency that requires a specific permission.
    
    Args:
        permission: Permission string to check
        
    Returns:
        Dependency function
    """
    async def permission_dependency(current_user: User = Depends(get_current_active_user)) -> User:
        if not current_user.has_permission(permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        return current_user
    
    return permission_dependency


def require_role(role: "UserRole"):
    """
    Create a dependency that requires a specific role or higher.
    
    Args:
        role: UserRole enum value
        
    Returns:
        Dependency function
    """
    async def role_dependency(current_user: User = Depends(get_current_active_user)) -> User:
        if not current_user.has_role(role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role.value}' or higher required"
            )
        return current_user
    
    return role_dependency