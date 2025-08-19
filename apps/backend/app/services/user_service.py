"""
User service for user-related operations.
"""

from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.models.models import User, Activity
from app.core.security import get_password_hash, verify_password


class UserService:
    """Service for user-related operations."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user."""
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            hashed_password=get_password_hash(user_data["password"]),
            full_name=user_data.get("full_name"),
            is_active=user_data.get("is_active", True),
            is_superuser=user_data.get("is_superuser", False)
        )
        
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        
        return user
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        user = self.db_session.query(User).filter(
            User.username == username
        ).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def update_profile(self, user_id: int, update_data: Dict[str, Any]) -> User:
        """Update user profile."""
        user = self.db_session.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise ValueError("User not found")
        
        for field, value in update_data.items():
            if hasattr(user, field) and field != "id":
                setattr(user, field, value)
        
        self.db_session.commit()
        self.db_session.refresh(user)
        
        return user
    
    def get_user_activities(self, user_id: int) -> List[Activity]:
        """Get all activities created by a user."""
        return self.db_session.query(Activity).filter(
            Activity.creator_id == user_id
        ).all()