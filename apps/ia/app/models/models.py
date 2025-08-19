"""
SQLAlchemy models for the application
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with profile
    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    """User profile model for activity matching."""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Profile data for activity matching
    skills = Column(JSON, default=list)  # List of skills: ['elevage', 'hygiene', etc.]
    preferences = Column(JSON, default=list)  # Category preferences: ['agri', 'transfo', etc.]
    availability = Column(JSON, default=list)  # Availability: ['weekend', 'semaine', etc.]
    location = Column(String(255), nullable=True)  # User location
    experience_level = Column(String(50), default="debutant")  # debutant, intermediaire, avance
    
    # Additional profile information
    bio = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with user
    user = relationship("User", back_populates="profile")


class Activity(Base):
    """Activity model for the 30 available activities."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    duration_min = Column(Integer, nullable=False)
    skill_tags = Column(JSON, default=list)  # Required skills
    seasonality = Column(JSON, default=list)  # When activity is available
    safety_level = Column(Integer, default=1)  # 1-3 safety level
    materials = Column(JSON, default=list)  # Required materials
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ActivityRecommendation(Base):
    """Store AI-generated recommendations for users."""
    __tablename__ = "activity_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    score = Column(Integer, nullable=False)  # Matching score 0-100
    reasons = Column(JSON, default=list)  # List of recommendation reasons
    ai_explanation = Column(Text, nullable=True)  # OpenAI generated explanation
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    activity = relationship("Activity")