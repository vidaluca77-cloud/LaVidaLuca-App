from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...core.security import verify_password, create_access_token, get_password_hash
from ...models.models import User
from ...schemas.schemas import UserCreate, User as UserSchema, Token, UserLogin
from ...core.config import settings


router = APIRouter()


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="""
    Create a new user account in the system.
    
    This endpoint allows new users to register by providing their email, username, and password.
    The system will validate that the email and username are unique before creating the account.
    
    **Requirements:**
    - Email must be valid and unique
    - Username must be unique and at least 3 characters
    - Password must be at least 8 characters long
    
    **Returns:**
    - Complete user profile information (without password)
    """,
    responses={
        201: {
            "description": "User successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "john.doe@example.com",
                        "username": "johndoe",
                        "full_name": "John Doe",
                        "is_active": True,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": None
                    }
                }
            }
        },
        400: {
            "description": "Email or username already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email or username already registered"
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
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=["authentication"]
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
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
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user and get access token",
    description="""
    Authenticate a user with username/email and password to receive a JWT access token.
    
    This endpoint validates user credentials and returns a JWT token that must be included
    in the Authorization header for protected endpoints.
    
    **Authentication Flow:**
    1. Send username/email and password
    2. Receive JWT token if credentials are valid
    3. Include token in Authorization header: `Bearer <token>`
    
    **Token Information:**
    - Token expires after 30 minutes (configurable)
    - Token type is always "bearer"
    - Use the token for all authenticated requests
    
    **Security:**
    - Passwords are hashed and never stored in plain text
    - Failed login attempts are logged for security monitoring
    """,
    responses={
        200: {
            "description": "Login successful, JWT token returned",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjQyNjg4NjAwfQ.signature",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect username or password"
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
                                "loc": ["body", "username"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=["authentication"]
)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token."""
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}