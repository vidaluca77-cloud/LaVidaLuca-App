from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...api.deps import get_current_active_user
from ...models.models import User
from ...schemas.schemas import User as UserSchema


router = APIRouter()


@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get current user profile",
    description="""
    Retrieve the profile information for the currently authenticated user.
    
    This endpoint returns complete user profile data for the logged-in user
    including account metadata and preferences.
    
    **Authentication Required:**
    - Must be logged in with valid JWT token
    - Returns data only for the authenticated user
    
    **Use Cases:**
    - Display user profile in the application
    - Get user information for personalization
    - Verify current authentication status
    
    **Security:**
    - Sensitive data like passwords are never included in responses
    - Only the authenticated user can access their own profile
    """,
    responses={
        200: {
            "description": "User profile successfully retrieved",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "john.doe@example.com",
                        "username": "johndoe",
                        "full_name": "John Doe",
                        "is_active": True,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-20T14:45:00Z"
                    }
                }
            }
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        }
    },
    tags=["users"]
)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get the profile of the currently authenticated user."""
    return current_user


@router.get(
    "/",
    response_model=List[UserSchema],
    summary="Get list of users",
    description="""
    Retrieve a list of user profiles with appropriate access control.
    
    This endpoint provides access to user information based on the
    requesting user's permissions and role.
    
    **Access Control:**
    - **Regular Users**: Can only see their own profile
    - **Superusers**: Can see all user profiles with pagination
    
    **Pagination:**
    - Use `skip` parameter to offset results
    - Use `limit` parameter to control the number of results
    - Default limit is 100 users per request
    
    **Use Cases:**
    - Admin user management interfaces
    - User directory for collaboration features
    - Moderation and user oversight
    
    **Privacy:**
    - Only basic profile information is included
    - Sensitive data is never exposed
    - Users can only access data appropriate to their role
    """,
    responses={
        200: {
            "description": "User list successfully retrieved",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "email": "john.doe@example.com",
                            "username": "johndoe",
                            "full_name": "John Doe",
                            "is_active": True,
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-20T14:45:00Z"
                        },
                        {
                            "id": 2,
                            "email": "jane.smith@example.com",
                            "username": "janesmith",
                            "full_name": "Jane Smith",
                            "is_active": True,
                            "created_at": "2024-01-16T09:15:00Z",
                            "updated_at": None
                        }
                    ]
                }
            }
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        }
    },
    tags=["users"]
)
def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of users based on current user's permissions."""
    # Only superusers can list all users
    if not current_user.is_superuser:
        return [current_user]
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users