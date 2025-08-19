"""
Activity model for educational activities and learning experiences.
"""

from sqlalchemy import Column, String, Text, Integer, Float, JSON, DateTime, Boolean, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .base import Base, BaseEntityMixin


class Activity(Base, BaseEntityMixin):
    """Activity model for educational activities."""
    
    __tablename__ = "activities"
    
    # Basic information
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text)
    
    # Activity details
    duration_min = Column(Integer, nullable=False)  # Duration in minutes
    skill_tags = Column(ARRAY(String), default=list)  # Skills/competencies
    safety_level = Column(Integer, default=1)  # 1=very safe, 5=risky
    materials = Column(ARRAY(String), default=list)  # Required materials
    
    # Difficulty and requirements
    difficulty_level = Column(Integer, default=1, index=True)  # 1=beginner, 5=expert
    min_participants = Column(Integer, default=1)
    max_participants = Column(Integer)
    age_min = Column(Integer)
    age_max = Column(Integer)
    
    # Location and logistics
    location_type = Column(String(50))  # indoor, outdoor, field, workshop
    location_details = Column(Text)
    preparation_time = Column(Integer, default=0)  # Preparation time in minutes
    
    # Educational aspects
    learning_objectives = Column(ARRAY(String), default=list)
    assessment_methods = Column(ARRAY(String), default=list)
    pedagogical_notes = Column(Text)
    
    # Metadata
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))  # Reference to user who created
    is_published = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False, index=True)
    
    # Search and categorization
    keywords = Column(ARRAY(String), default=list)
    season_tags = Column(ARRAY(String), default=list)  # spring, summer, autumn, winter
    
    # Additional data
    external_resources = Column(JSON, default=dict)  # Links, references
    metadata = Column(JSON, default=dict)  # Flexible additional data
    
    # Relationships
    creator = relationship("User", back_populates="activities")
    
    def __repr__(self):
        return f"<Activity(id={self.id}, title={self.title}, category={self.category})>"
    
    def to_dict(self):
        """Convert activity to dictionary."""
        data = super().to_dict()
        return data


# Create indexes for search optimization
Index('ix_activities_title_search', Activity.title)
Index('ix_activities_category_published', Activity.category, Activity.is_published)
Index('ix_activities_difficulty_published', Activity.difficulty_level, Activity.is_published)
Index('ix_activities_duration', Activity.duration_min)
Index('ix_activities_age_range', Activity.age_min, Activity.age_max)
Index('ix_activities_creator', Activity.created_by)