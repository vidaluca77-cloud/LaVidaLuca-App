"""
User model for La Vida Luca application.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """
    User model for storing user information and preferences.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # User profile information
    skills = Column(JSON, default=list)  # List of skill tags
    availability = Column(JSON, default=list)  # Availability preferences
    location = Column(String(255), nullable=True)
    preferences = Column(JSON, default=list)  # Category preferences
    
    # Additional profile data
    bio = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Metadata
    is_active = Column(Integer, default=1)  # Using Integer for SQLite compatibility
    is_verified = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.full_name}')>"