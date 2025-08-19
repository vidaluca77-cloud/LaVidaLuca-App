"""User service."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..models.user import User, UserRole
from ..schemas.user import UserCreate, UserUpdate


class UserService:
    """User service."""

    @staticmethod
    def get_user(db: Session, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users with pagination."""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create new user."""
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            role=user_create.role,
            phone=user_create.phone,
            bio=user_create.bio,
            location=user_create.location,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user: User, user_update: UserUpdate) -> User:
        """Update user."""
        user_data = user_update.dict(exclude_unset=True)
        for field, value in user_data.items():
            setattr(user, field, value)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        """Delete user."""
        db.delete(user)
        db.commit()

    @staticmethod
    def update_password(db: Session, user: User, new_password: str) -> None:
        """Update user password."""
        hashed_password = get_password_hash(new_password)
        user.hashed_password = hashed_password
        db.add(user)
        db.commit()

    @staticmethod
    def get_users_by_role(db: Session, role: UserRole) -> List[User]:
        """Get users by role."""
        return db.query(User).filter(User.role == role).all()

    @staticmethod
    def get_active_users(db: Session) -> List[User]:
        """Get active users."""
        return db.query(User).filter(User.is_active == True).all()

    @staticmethod
    def get_user_statistics(db: Session, user: User) -> dict:
        """Get user statistics."""
        total_bookings = len(user.bookings)
        completed_activities = len([p for p in user.progress_records])
        
        # Calculate total time spent
        total_time = sum(p.time_spent_minutes or 0 for p in user.progress_records)
        
        # Get unique skills
        skills = set()
        for progress in user.progress_records:
            skills.update(progress.skills_gained or [])
        
        return {
            "total_bookings": total_bookings,
            "completed_activities": completed_activities,
            "total_time_spent": total_time,
            "skills_acquired": list(skills),
        }