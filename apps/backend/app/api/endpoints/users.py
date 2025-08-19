from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...api.deps import get_current_active_user
from ...models.models import User
from ...schemas.schemas import User as UserSchema


router = APIRouter()


@router.get("/me", response_model=UserSchema, summary="Get current user profile")
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get the profile information for the currently authenticated user.
    
    **Authentication required.** Returns the user's profile information
    including email, username, full name, and account status.
    
    This endpoint is useful for displaying user information in the UI
    and checking the current user's permissions.
    """
    return current_user


@router.get("/", response_model=List[UserSchema], summary="List users")
def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of users to return"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List users in the system.
    
    **Authentication required.** 
    
    **Permissions:**
    - Regular users: Returns only their own user information
    - Superusers: Returns a paginated list of all users
    
    **Parameters:**
    - **skip**: Number of users to skip for pagination
    - **limit**: Maximum number of users to return (1-100)
    """
    # Only superusers can list all users
    if not current_user.is_superuser:
        return [current_user]
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users