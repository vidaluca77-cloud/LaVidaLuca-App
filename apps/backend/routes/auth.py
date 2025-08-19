"""
Authentication routes for login, registration, and token management.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db_session
from ..models.user import User
from ..schemas.auth import UserLogin, UserRegister, TokenPair, RefreshTokenRequest
from ..schemas.user import UserResponse
from ..schemas.common import ApiResponse
from ..auth.password import hash_password, verify_password
from ..auth.jwt import jwt_handler
from ..auth.oauth import oauth_manager
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


@router.post("/login", response_model=ApiResponse[TokenPair])
async def login_user(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Authenticate user and return access and refresh tokens.
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
    user_data = {"sub": str(user.id), "email": user.email}
    
    access_token, refresh_token = jwt_handler.create_token_pair(user_data)
    
    # Store refresh token
    await jwt_handler.store_refresh_token(db, str(user.id), refresh_token)
    
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    await db.commit()
    
    return ApiResponse(
        success=True,
        data=TokenPair(
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


@router.post("/refresh", response_model=ApiResponse[TokenPair])
async def refresh_access_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Refresh access token using refresh token.
    """
    # Verify refresh token
    user_id = await jwt_handler.verify_refresh_token(db, request.refresh_token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # Get user data
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new token pair
    user_data = {"sub": str(user.id), "email": user.email}
    access_token, new_refresh_token = jwt_handler.create_token_pair(user_data)
    
    # Store new refresh token (this will revoke the old one)
    await jwt_handler.store_refresh_token(db, str(user.id), new_refresh_token)
    
    access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    
    return ApiResponse(
        success=True,
        data=TokenPair(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=int(access_token_expires.total_seconds())
        ),
        message="Token refreshed successfully"
    )


@router.post("/logout", response_model=ApiResponse[dict])
async def logout_user(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout user by revoking refresh token.
    """
    # Revoke the refresh token
    await jwt_handler.revoke_refresh_token(db, request.refresh_token)
    
    return ApiResponse(
        success=True,
        data={"message": "Logged out successfully"},
        message="Logout successful"
    )


# OAuth Routes

@router.get("/oauth/providers", response_model=ApiResponse[list])
async def get_oauth_providers():
    """
    Get available OAuth providers.
    """
    providers = oauth_manager.get_available_providers()
    return ApiResponse(
        success=True,
        data=providers,
        message="Available OAuth providers"
    )


@router.get("/oauth/{provider}/authorize")
async def oauth_authorize(
    provider: str,
    redirect_url: str = None
):
    """
    Start OAuth authorization flow.
    """
    oauth_provider = oauth_manager.get_provider(provider)
    if not oauth_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OAuth provider '{provider}' not found"
        )
    
    # Create state for CSRF protection
    state = oauth_manager.create_oauth_state(provider, redirect_url)
    
    # Get authorization URL
    auth_url = oauth_provider.get_authorization_url(state)
    
    return {"authorization_url": auth_url, "state": state}


@router.get("/oauth/{provider}/callback", response_model=ApiResponse[TokenPair])
async def oauth_callback(
    provider: str,
    code: str,
    state: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Handle OAuth callback and complete authentication.
    """
    # Verify state
    state_data = oauth_manager.verify_oauth_state(state, provider)
    if not state_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OAuth state"
        )
    
    # Get OAuth provider
    oauth_provider = oauth_manager.get_provider(provider)
    if not oauth_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OAuth provider '{provider}' not found"
        )
    
    try:
        # Exchange code for access token
        access_token = await oauth_provider.get_access_token(code, state)
        
        # Get user info
        user_info = await oauth_provider.get_user_info(access_token)
        
        # Find or create user
        user = await _find_or_create_oauth_user(db, user_info)
        
        # Create token pair
        user_data = {"sub": str(user.id), "email": user.email}
        access_token, refresh_token = jwt_handler.create_token_pair(user_data)
        
        # Store refresh token
        await jwt_handler.store_refresh_token(db, str(user.id), refresh_token)
        
        # Update last login
        from datetime import datetime
        user.last_login = datetime.utcnow()
        await db.commit()
        
        access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        
        return ApiResponse(
            success=True,
            data=TokenPair(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=int(access_token_expires.total_seconds())
            ),
            message="OAuth authentication successful"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}"
        )


async def _find_or_create_oauth_user(db: AsyncSession, user_info: dict) -> User:
    """
    Find existing user or create new user from OAuth data.
    """
    email = user_info.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required from OAuth provider"
        )
    
    # Try to find existing user by email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if user:
        # Update OAuth info in profile
        if not user.profile:
            user.profile = {}
        
        provider = user_info.get("provider")
        user.profile[f"{provider}_id"] = user_info.get("provider_id")
        user.profile[f"{provider}_picture"] = user_info.get("picture")
        
        if user_info.get("verified"):
            user.is_verified = True
        
        await db.commit()
        return user
    
    # Create new user
    new_user = User(
        email=email,
        hashed_password="",  # OAuth users don't need a password
        first_name=user_info.get("first_name"),
        last_name=user_info.get("last_name"),
        is_verified=user_info.get("verified", False),
        profile={
            f"{user_info.get('provider')}_id": user_info.get("provider_id"),
            f"{user_info.get('provider')}_picture": user_info.get("picture"),
            "oauth_provider": user_info.get("provider"),
            "username": user_info.get("username")
        }
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user