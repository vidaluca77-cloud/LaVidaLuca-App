"""
Database models for La Vida Luca application.
Defines User and Activity models with SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid

class User(Base):
    """User model for authentication and profiles."""
    
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: f"user_{uuid.uuid4().hex[:8]}")
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Profile information stored as JSON
    profile = Column(JSON, default={})
    
    # Relationship to activities (if user creates activities)
    created_activities = relationship("Activity", back_populates="creator")

class Activity(Base):
    """Activity model for educational activities."""
    
    __tablename__ = "activities"
    
    id = Column(String, primary_key=True, default=lambda: f"act_{uuid.uuid4().hex[:8]}")
    title = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text)
    duration_min = Column(Integer, nullable=False)  # Duration in minutes
    
    # Skills and materials as JSON arrays
    skill_tags = Column(JSON, default=[])
    materials = Column(JSON, default=[])
    
    # Safety and difficulty
    safety_level = Column(Integer, default=3)  # 1-5 scale
    difficulty_level = Column(Integer, default=3)  # 1-5 scale
    
    # Location and availability
    location = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Creator relationship
    creator_id = Column(String, ForeignKey("users.id"))
    creator = relationship("User", back_populates="created_activities")
    
    # Metadata for AI suggestions
    engagement_score = Column(Float, default=0.0)  # How engaging the activity is
    success_rate = Column(Float, default=0.0)  # Success rate among participants