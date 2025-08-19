"""
Database models for La Vida Luca application.
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from .database import Base


def generate_id():
    """Generate a unique ID."""
    return str(uuid.uuid4())


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_id)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Optional for Supabase users
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Profile data
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    skills = Column(JSON, default=list)  # List of skill strings
    availability = Column(JSON, default=list)  # List of availability strings
    location = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    
    # Relationships
    user_activities = relationship("UserActivity", back_populates="user")


class Activity(Base):
    """Activity model."""
    __tablename__ = "activities"
    
    id = Column(String, primary_key=True, default=generate_id)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    duration_min = Column(Integer, nullable=False)
    skill_tags = Column(JSON, default=list)  # List of skill strings
    safety_level = Column(Integer, nullable=False, default=1)  # 1-5 scale
    materials = Column(JSON, default=list)  # List of material strings
    location_type = Column(String, nullable=True)  # indoor, outdoor, flexible
    season = Column(JSON, default=list)  # List of seasons
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Creator info (optional)
    created_by = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user_activities = relationship("UserActivity", back_populates="activity")


class UserActivity(Base):
    """User-Activity relationship model for tracking completions, favorites, etc."""
    __tablename__ = "user_activities"
    
    id = Column(String, primary_key=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    activity_id = Column(String, ForeignKey("activities.id"), nullable=False)
    
    # Interaction type
    interaction_type = Column(String, nullable=False)  # completed, favorited, interested
    
    # Completion data
    completed_at = Column(DateTime, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 stars
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_activities")
    activity = relationship("Activity", back_populates="user_activities")


class Suggestion(Base):
    """AI-generated suggestions for users."""
    __tablename__ = "suggestions"
    
    id = Column(String, primary_key=True, default=generate_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    activity_id = Column(String, ForeignKey("activities.id"), nullable=False)
    
    # Suggestion data
    score = Column(Float, nullable=False)  # 0.0 - 1.0 relevance score
    reasons = Column(JSON, default=list)  # List of reason strings
    ai_model = Column(String, nullable=True)  # Model used for generation
    
    # Interaction
    viewed = Column(Boolean, default=False)
    clicked = Column(Boolean, default=False)
    dismissed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)  # Optional expiration


class ContactMessage(Base):
    """Contact form messages."""
    __tablename__ = "contact_messages"
    
    id = Column(String, primary_key=True, default=generate_id)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    status = Column(String, default="new")  # new, read, responded
    created_at = Column(DateTime, default=func.now())