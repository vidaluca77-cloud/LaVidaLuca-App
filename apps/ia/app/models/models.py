"""
Database models for La Vida Luca application
"""

from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    recommendations = relationship("Recommendation", back_populates="user")


class UserProfile(Base):
    """User profile model with preferences and skills"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Profile information
    skills = Column(JSON, default=[])
    availability = Column(JSON, default=[])
    location = Column(String)
    preferences = Column(JSON, default=[])
    bio = Column(Text)
    
    # MFR specific
    mfr_level = Column(String)  # beginner, intermediate, advanced
    age_range = Column(String)  # young, adult
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")


class Activity(Base):
    """Activity model based on the 30 predefined activities"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text)
    description = Column(Text)
    
    # Activity properties
    duration_min = Column(Integer)
    skill_tags = Column(JSON, default=[])
    seasonality = Column(JSON, default=[])
    safety_level = Column(Integer, default=1)  # 1-5 scale
    materials = Column(JSON, default=[])
    
    # Additional properties
    difficulty_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    max_participants = Column(Integer)
    location_type = Column(String)  # indoor, outdoor, both
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recommendations = relationship("Recommendation", back_populates="activity")


class Recommendation(Base):
    """AI-generated recommendations for users"""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    
    # Recommendation data
    score = Column(Float, nullable=False)  # 0.0-1.0 confidence score
    reasons = Column(JSON, default=[])
    ai_explanation = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    activity = relationship("Activity", back_populates="recommendations")


class ActivitySession(Base):
    """Track user participation in activities"""
    __tablename__ = "activity_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    
    # Session data
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    satisfaction_rating = Column(Integer, nullable=True)  # 1-5 stars
    feedback = Column(Text)
    
    # Status
    status = Column(String, default="started")  # started, completed, abandoned
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())