"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.dependencies import standard_rate_limit, auth_rate_limit
from ...core.security import get_current_active_user
from ...db.session import get_db
from ...models.user import User
from ...schemas.user import (
    Token, LoginRequest, RegisterRequest, User as UserSchema,
    ChangePassword
)
from ...services.auth import AuthService
from ...services.email import EmailService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=Token)
@auth_rate_limit
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    
    # Validate password confirmation
    if register_data.password != register_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    auth_service = AuthService(db)
    email_service = EmailService()
    
    # Register user
    result = auth_service.register(register_data)
    
    # Send welcome email (don't fail if email fails)
    try:
        await email_service.send_welcome_email(
            register_data.email,
            register_data.first_name or register_data.email.split("@")[0]
        )
    except Exception:
        pass  # Email failure shouldn't block registration
    
    return result


@router.post("/login", response_model=Token)
@auth_rate_limit
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login user and return access token."""
    
    auth_service = AuthService(db)
    return auth_service.login(login_data)


@router.get("/me", response_model=UserSchema)
@standard_rate_limit
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information."""
    return current_user


@router.post("/change-password")
@auth_rate_limit
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change user password."""
    
    # Validate password confirmation
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match"
        )
    
    auth_service = AuthService(db)
    auth_service.change_password(
        current_user,
        password_data.current_password,
        password_data.new_password
    )
    
    return {"message": "Password changed successfully"}


@router.post("/deactivate")
@auth_rate_limit
async def deactivate_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Deactivate user account."""
    
    auth_service = AuthService(db)
    auth_service.deactivate_user(current_user)
    
    return {"message": "Account deactivated successfully"}