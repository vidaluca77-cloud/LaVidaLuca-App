from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.database import Base
from datetime import datetime
import json


def get_array_column(item_type=String):
    """Get array column that works with both PostgreSQL and SQLite."""
    try:
        # Try PostgreSQL ARRAY type first
        return ARRAY(item_type)
    except:
        # Fallback to JSON for SQLite
        return JSON


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    location = Column(String)
    
    # Profile data stored as arrays (JSON for SQLite compatibility)
    skills = Column(JSON, default=list)
    availability = Column(JSON, default=list)
    preferences = Column(JSON, default=list)
    
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Activity relationships
    recommendations = relationship("Recommendation", back_populates="user")


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # 'agri', 'transfo', 'artisanat', 'nature', 'social'
    summary = Column(Text)
    description = Column(Text)
    duration_min = Column(Integer, nullable=False)
    skill_tags = Column(JSON, default=list)
    seasonality = Column(JSON, default=list)
    safety_level = Column(Integer, nullable=False)
    materials = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recommendations = relationship("Recommendation", back_populates="activity")


class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    score = Column(Float, nullable=False)
    reasons = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    activity = relationship("Activity", back_populates="recommendations")