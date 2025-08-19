"""
User model.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.base import Base


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    role = Column(String(50), default="student", nullable=False)  # student, instructor, moderator, admin
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Profile information
    bio = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Structured profile data
    profile_data = Column(JSON, nullable=True)  # skills, availability, preferences
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    submissions = relationship("ActivitySubmission", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.email.split("@")[0]
    
    @property
    def is_instructor_or_above(self) -> bool:
        """Check if user has instructor privileges or higher."""
        return self.role in ["instructor", "moderator", "admin"]
    
    @property
    def is_moderator_or_above(self) -> bool:
        """Check if user has moderator privileges or higher."""
        return self.role in ["moderator", "admin"]
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == "admin"