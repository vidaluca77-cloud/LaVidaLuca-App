from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import (
    verify_password, get_password_hash, create_access_token, verify_token
)
from app.core.config import settings
from app.models import User as UserModel
from app.schemas import (
    User, UserCreate, UserUpdate, UserLogin, Token, UserInDB
)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/login")

router = APIRouter()


def get_user_by_username(db: Session, username: str) -> Optional[UserModel]:
    """Get user by username"""
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    """Get user by email"""
    return db.query(UserModel).filter(UserModel.email == email).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[UserModel]:
    """Authenticate user with username and password"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> UserModel:
    """Get current authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        school=user_data.school,
        level=user_data.level,
        bio=user_data.bio,
        phone=user_data.phone,
        location=user_data.location,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def get_current_user_info(current_user: UserModel = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user


@router.put("/me", response_model=User)
def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Handle password update separately
    if "password" in update_data:
        hashed_password = get_password_hash(update_data.pop("password"))
        update_data["hashed_password"] = hashed_password
    
    # Check for unique constraints
    if "email" in update_data and update_data["email"] != current_user.email:
        if get_user_by_email(db, update_data["email"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    if "username" in update_data and update_data["username"] != current_user.username:
        if get_user_by_username(db, update_data["username"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Update user
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/", response_model=List[User])
def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all users (admin only or public profiles)"""
    users = db.query(UserModel).filter(UserModel.is_active == True).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Get user by ID"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user