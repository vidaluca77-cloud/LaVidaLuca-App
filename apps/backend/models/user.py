"""
User model for authentication and profile management.
"""

from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from ..database import Base


class UserRole(enum.Enum):
    """User roles enumeration."""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPERUSER = "superuser"


class User(Base):
    """User model for authentication and profiles."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile information
    first_name = Column(String(100))
    last_name = Column(String(100))
    profile = Column(JSON, default=dict)  # Flexible profile data
    
    # User status and roles
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role.value})>"
    
    @property
    def full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
    
    def has_role(self, role: UserRole) -> bool:
        """Check if user has specific role or higher."""
        role_hierarchy = {
            UserRole.USER: 0,
            UserRole.MODERATOR: 1,
            UserRole.ADMIN: 2,
            UserRole.SUPERUSER: 3
        }
        
        user_level = role_hierarchy.get(self.role, 0)
        required_level = role_hierarchy.get(role, 0)
        
        return user_level >= required_level
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission based on role."""
        permissions = {
            UserRole.USER: [
                "read_own_profile",
                "update_own_profile",
                "create_activities",
                "read_activities",
            ],
            UserRole.MODERATOR: [
                "read_own_profile",
                "update_own_profile",
                "create_activities",
                "read_activities",
                "moderate_activities",
                "moderate_comments",
            ],
            UserRole.ADMIN: [
                "read_own_profile",
                "update_own_profile",
                "create_activities",
                "read_activities",
                "moderate_activities",
                "moderate_comments",
                "manage_users",
                "read_analytics",
                "system_settings",
            ],
            UserRole.SUPERUSER: [
                "*"  # All permissions
            ]
        }
        
        user_permissions = permissions.get(self.role, [])
        return "*" in user_permissions or permission in user_permissions
    
    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)."""
        return {
            "id": str(self.id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "profile": self.profile,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "role": self.role.value if self.role else UserRole.USER.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }