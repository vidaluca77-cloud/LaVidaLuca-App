"""Authentication routes for user registration and login."""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, settings
from auth import authenticate_user, create_user, get_user_by_email, create_access_token, get_current_active_user
import schemas

router = APIRouter()

@router.post("/register", response_model=schemas.SuccessResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = create_user(db=db, user=user)
    
    return schemas.SuccessResponse(
        data={"user_id": new_user.id, "email": new_user.email},
        message="User registered successfully"
    )

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

@router.put("/me", response_model=schemas.SuccessResponse)
async def update_user_profile(
    user_update: schemas.UserUpdate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    if user_update.profile:
        current_user.profile = user_update.profile.dict()
        db.commit()
        db.refresh(current_user)
    
    return schemas.SuccessResponse(
        data={"user_id": current_user.id},
        message="Profile updated successfully"
    )