from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.core.models import User, UserProfile
from app.schemas.schemas import UserCreate, UserUpdate, UserProfileCreate, UserProfileUpdate
from app.auth.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_username_or_email(self, username_or_email: str) -> Optional[User]:
        """Get user by username or email"""
        return self.db.query(User).filter(
            or_(User.username == username_or_email, User.email == username_or_email)
        ).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user_create: UserCreate) -> User:
        """Create new user"""
        # Check if user already exists
        if self.get_user_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        if self.get_user_by_username(user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Create user
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            location=user_create.location,
            is_mfr_student=user_create.is_mfr_student
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        # Create empty profile
        self.create_user_profile(db_user.id, UserProfileCreate())
        
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user"""
        db_user = self.get_user(user_id)
        if not db_user:
            return None

        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = self.get_user_by_username_or_email(username_or_email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate user"""
        db_user = self.get_user(user_id)
        if not db_user:
            return None

        db_user.is_active = False
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_profile(self, user_id: int) -> Optional[UserProfile]:
        """Get user profile"""
        return self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    def create_user_profile(self, user_id: int, profile_create: UserProfileCreate) -> UserProfile:
        """Create user profile"""
        db_profile = UserProfile(
            user_id=user_id,
            **profile_create.dict()
        )
        
        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)
        return db_profile

    def update_user_profile(self, user_id: int, profile_update: UserProfileUpdate) -> Optional[UserProfile]:
        """Update user profile"""
        db_profile = self.get_user_profile(user_id)
        if not db_profile:
            return None

        update_data = profile_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_profile, field, value)

        self.db.commit()
        self.db.refresh(db_profile)
        return db_profile