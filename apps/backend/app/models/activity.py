from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float
from sqlalchemy.sql import func
from ..core.database import Base

class Activity(Base):
    """Activity model for the 30 activities catalog"""
    
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)  # Extended description
    
    # Activity metadata
    duration_min = Column(Integer, nullable=False)  # Duration in minutes
    skill_tags = Column(JSON, default=list)  # Required/developed skills
    seasonality = Column(JSON, default=list)  # When activity is available
    safety_level = Column(Integer, default=1)  # 1-3 safety level
    materials = Column(JSON, default=list)  # Required materials
    
    # Location and capacity
    location_type = Column(String(100), nullable=True)  # farm, workshop, outdoor, etc.
    max_participants = Column(Integer, default=10)
    min_age = Column(Integer, default=14)
    
    # Status and visibility
    is_active = Column(Boolean, default=True)
    is_mfr_only = Column(Boolean, default=False)  # Reserved for MFR students
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional fields for recommendations
    difficulty_level = Column(Integer, default=1)  # 1-5 difficulty
    learning_objectives = Column(JSON, default=list)
    prerequisites = Column(JSON, default=list)
    
    def __repr__(self):
        return f"<Activity(id={self.id}, slug='{self.slug}', title='{self.title}', category='{self.category}')>"