"""
User model for authentication and profile management.
"""

from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .base import Base, BaseEntityMixin


class User(Base, BaseEntityMixin):
    """User model for authentication and profiles."""
    
    __tablename__ = "users"
    
    # Authentication fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Role-based access
    role = Column(String(50), default="user", nullable=False)  # user, admin, moderator
    
    # Profile information
    first_name = Column(String(100))
    last_name = Column(String(100))
    profile = Column(JSON, default=dict)  # Flexible profile data
    
    # User status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Login tracking
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    activities = relationship("Activity", back_populates="creator")
    assigned_contacts = relationship("Contact", back_populates="assigned_user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
    
    @property
    def full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
    
    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)."""
        data = super().to_dict(exclude_fields=['hashed_password'])
        data['full_name'] = self.full_name
        return data


# Create indexes for search optimization
Index('ix_users_email_active', User.email, User.is_active)
Index('ix_users_role', User.role)
Index('ix_users_last_login', User.last_login)