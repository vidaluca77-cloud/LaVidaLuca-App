"""
User model for La Vida Luca application.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
import uuid

from ..core.database import Base


class User(Base):
    """User model for authentication and profile management."""
    
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    bio = Column(Text)
    location = Column(String)
    phone = Column(String)
    
    # Profile information
    institution = Column(String)  # MFR or organization
    role = Column(String, default="student")  # student, teacher, coordinator, admin
    expertise_areas = Column(Text)  # JSON string of expertise areas
    interests = Column(Text)  # JSON string of interests
    
    # Status fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relationships
    created_activities = relationship("Activity", back_populates="creator", foreign_keys="Activity.creator_id")
    activity_suggestions = relationship("ActivitySuggestion", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def display_name(self):
        return self.full_name or self.username