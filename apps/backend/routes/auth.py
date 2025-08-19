"""
Authentication routes for login, registration, and token management.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db_session
from ..models.user import User
from ..schemas.auth import UserLogin, UserRegister, Token
from ..schemas.user import UserResponse
from ..schemas.common import ApiResponse
from ..auth.password import hash_password, verify_password
from ..auth.jwt_handler import create_access_token
from ..auth.dependencies import get_current_active_user
from ..config import settings


router = APIRouter()


@router.post(
    "/register", 
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="Create a new user account with email, password, and optional profile information.",
    responses={
        201: {
            "description": "User successfully registered",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "id": "uuid-string",
                            "email": "user@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "is_active": True,
                            "created_at": "2024-01-01T00:00:00Z"
                        },
                        "message": "User registered successfully"
                    }
                }
            }
        },
        400: {
            "description": "Bad request - Email already registered or validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email already registered"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "password"],
                                "msg": "Password must contain at least one uppercase letter",
                                "type": "value_error"
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=["Authentication"]
)
async def register_user(
    user_data: UserRegister = Field(
        ...,
        example={
            "email": "user@example.com",
            "password": "SecurePass123",
            "first_name": "John",
            "last_name": "Doe"
        }
    ),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Register a new user account.
    
    This endpoint allows new users to create an account by providing:
    - Email address (must be unique)
    - Password (minimum 8 characters with complexity requirements)
    - Optional first and last name
    
    **Rate Limit:** 5 requests per minute per IP
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


@router.post(
    "/login", 
    response_model=ApiResponse[Token],
    summary="Authenticate user and get access token",
    description="Login with email and password to receive a JWT access token for API authentication.",
    responses={
        200: {
            "description": "Successfully authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            "token_type": "bearer",
                            "expires_in": 86400
                        },
                        "message": "Login successful"
                    }
                }
            }
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect email or password"
                    }
                }
            }
        },
        400: {
            "description": "Inactive user account",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Inactive user account"
                    }
                }
            }
        }
    },
    tags=["Authentication"]
)
async def login_user(
    user_credentials: UserLogin = Field(
        ...,
        example={
            "email": "user@example.com",
            "password": "SecurePass123"
        }
    ),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Authenticate user and return access token.
    
    This endpoint validates user credentials and returns a JWT access token that can be used
    to authenticate subsequent API requests.
    
    **Rate Limit:** 10 requests per minute per IP
    **Token Expiry:** 24 hours
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
    
    # Create access token
    access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    access_token = create_access_token(
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
            token_type="bearer",
            expires_in=int(access_token_expires.total_seconds())
        ),
        message="Login successful"
    )


@router.post(
    "/verify-token", 
    response_model=ApiResponse[UserResponse],
    summary="Verify JWT token and get user information",
    description="Validate the provided JWT token and return the authenticated user's information.",
    responses={
        200: {
            "description": "Token is valid",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "id": "uuid-string",
                            "email": "user@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "is_active": True,
                            "created_at": "2024-01-01T00:00:00Z"
                        },
                        "message": "Token is valid"
                    }
                }
            }
        },
        401: {
            "description": "Invalid or expired token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Could not validate credentials"
                    }
                }
            }
        }
    },
    tags=["Authentication"],
    dependencies=[Depends(get_current_active_user)]
)
async def verify_token_endpoint(
    current_user: User = Depends(get_current_active_user)
):
    """
    Verify the current token and return user information.
    
    This endpoint validates a JWT token passed in the Authorization header
    and returns the authenticated user's profile information.
    
    **Authentication Required:** Bearer Token
    **Rate Limit:** 100 requests per minute per user
    """
    return ApiResponse(
        success=True,
        data=UserResponse.from_orm(current_user),
        message="Token is valid"
    )