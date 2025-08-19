"""
Authentication routes for login, registration, and token management.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db_session
from ..models.user import User
from ..schemas.auth import UserLogin, UserRegister, Token
from ..schemas.user import UserResponse
from ..schemas.common import ApiResponse
from ..auth.password import hash_password, verify_password
from ..auth.jwt_handler import create_tokens, refresh_access_token, revoke_refresh_token, revoke_all_user_tokens
from ..auth.dependencies import get_current_active_user
from ..config import settings


router = APIRouter()


@router.post("/register", response_model=ApiResponse[UserResponse])
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Register a new user account.
    """
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return ApiResponse(
        success=True,
        data=UserResponse.from_orm(new_user),
        message="User registered successfully"
    )


@router.post("/login", response_model=ApiResponse[Token])
async def login_user(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Authenticate user and return access and refresh tokens.
    
    Returns both access token (short-lived) and refresh token (long-lived)
    for secure session management.
    """
    # Find user by email
    result = await db.execute(select(User).where(User.email == user_credentials.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access and refresh tokens
    access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    access_token, refresh_token = create_tokens(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    await db.commit()
    
    return ApiResponse(
        success=True,
        data=Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=int(access_token_expires.total_seconds())
        ),
        message="Login successful"
    )


@router.post("/verify-token", response_model=ApiResponse[UserResponse])
async def verify_token_endpoint(
    current_user: User = Depends(get_current_active_user)
):
    """
    Verify the current token and return user information.
    """
    return ApiResponse(
        success=True,
        data=UserResponse.from_orm(current_user),
        message="Token is valid"
    )


@router.post("/refresh", response_model=ApiResponse[Token])
async def refresh_token_endpoint(
    refresh_token_data: dict
):
    """
    Generate a new access token using a valid refresh token.
    
    Expects JSON body with 'refresh_token' field.
    """
    refresh_token = refresh_token_data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required"
        )
    
    try:
        new_access_token = refresh_access_token(refresh_token)
        access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        
        return ApiResponse(
            success=True,
            data=Token(
                access_token=new_access_token,
                token_type="bearer",
                expires_in=int(access_token_expires.total_seconds())
            ),
            message="Token refreshed successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout", response_model=ApiResponse[dict])
async def logout_user(
    refresh_token_data: dict
):
    """
    Logout user by revoking the refresh token.
    
    Expects JSON body with 'refresh_token' field.
    """
    refresh_token = refresh_token_data.get("refresh_token")
    if refresh_token:
        revoke_refresh_token(refresh_token)
    
    return ApiResponse(
        success=True,
        data={},
        message="Logout successful"
    )


@router.post("/logout-all", response_model=ApiResponse[dict])
async def logout_all_sessions(
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout user from all sessions by revoking all refresh tokens.
    """
    revoked_count = revoke_all_user_tokens(str(current_user.id))
    
    return ApiResponse(
        success=True,
        data={"revoked_tokens": revoked_count},
        message=f"Logged out from {revoked_count} sessions"
    )