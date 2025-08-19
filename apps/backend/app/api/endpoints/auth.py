from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.sql import func

from ...core.database import get_db
from ...core.security import (
    verify_password, create_access_token, create_refresh_token, 
    get_password_hash, verify_token, get_current_user
)
from ...models import User
from ...schemas import (
    UserRegistration, User as UserSchema, Token, UserLogin,
    RefreshToken, PasswordReset, PasswordResetConfirm
)
from ...core.config import settings


router = APIRouter()


@router.post("/register", response_model=UserSchema)
async def register_user(user: UserRegistration, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    result = await db.execute(
        select(User).where(
            or_(User.email == user.email, User.username == user.username)
        )
    )
    db_user = result.scalar_one_or_none()
    
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        institution=user.institution,
        role=user.role,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
async def login_user(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return tokens."""
    result = await db.execute(
        select(User).where(
            or_(User.username == user_credentials.username, User.email == user_credentials.username)
        )
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user account"
        )
    
    # Update last login
    user.last_login = func.now()
    await db.commit()
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_data: RefreshToken, db: AsyncSession = Depends(get_db)):
    """Refresh access token using refresh token."""
    user_id = verify_token(refresh_data.refresh_token, token_type="refresh")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Verify user still exists and is active
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


@router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_user)):
    """Logout user (client should discard tokens)."""
    return {"message": "Successfully logged out"}