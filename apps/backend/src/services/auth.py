"""Authentication service."""

from typing import Optional

from sqlalchemy.orm import Session

from ..core.security import verify_password
from ..models.user import User


class AuthService:
    """Authentication service."""

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def is_user_active(user: User) -> bool:
        """Check if user is active."""
        return user.is_active

    @staticmethod
    def is_user_admin(user: User) -> bool:
        """Check if user is admin."""
        return user.role == "admin"

    @staticmethod
    def is_user_instructor_or_admin(user: User) -> bool:
        """Check if user is instructor or admin."""
        return user.role in ["instructor", "admin"]