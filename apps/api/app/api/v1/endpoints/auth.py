from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.core.config import settings
from app.schemas.schemas import UserCreate, Token, UserLogin, User
from app.services.user_service import UserService
from app.auth.security import create_access_token, create_refresh_token, verify_token

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: Request,  # Required for rate limiting
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    user_service = UserService(db)
    
    try:
        user = user_service.create_user(user_create)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(
    request: Request,  # Required for rate limiting
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT tokens"""
    user_service = UserService(db)
    
    user = user_service.authenticate_user(
        user_login.username_or_email, 
        user_login.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        subject=user.username, expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
@limiter.limit("20/minute")
async def refresh_token(
    request: Request,  # Required for rate limiting
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify refresh token
    username = verify_token(refresh_token, "refresh")
    if username is None:
        raise credentials_exception
    
    # Get user
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if user is None or not user.is_active:
        raise credentials_exception
    
    # Create new tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    new_access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(
        subject=user.username, expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }