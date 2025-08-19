"""
Activity model for La Vida Luca application.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..core.database import Base


class Activity(Base):
    """Activity model for educational activities."""
    
    __tablename__ = "activities"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    short_description = Column(String(255))
    
    # Categorization
    category = Column(String, nullable=False, index=True)  # agriculture, sustainability, etc.
    subcategory = Column(String)
    tags = Column(Text)  # JSON string of tags
    
    # Difficulty and requirements
    difficulty_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    duration_minutes = Column(Integer)
    max_participants = Column(Integer)
    min_age = Column(Integer)
    max_age = Column(Integer)
    
    # Location and setup
    location_type = Column(String)  # indoor, outdoor, field, lab, etc.
    location = Column(String)
    equipment_needed = Column(Text)  # JSON string of equipment
    preparation_time_minutes = Column(Integer)
    
    # Educational content
    learning_objectives = Column(Text)  # JSON string of objectives
    competencies_developed = Column(Text)  # JSON string of competencies
    prerequisites = Column(Text)
    assessment_methods = Column(Text)
    
    # Resources
    materials_provided = Column(Text)  # JSON string of materials
    additional_resources = Column(Text)  # JSON string of links/resources
    instructions = Column(Text)  # Detailed instructions
    
    # Metadata
    language = Column(String, default="fr")
    cost_estimate = Column(Float)  # Estimated cost in euros
    sustainability_score = Column(Integer)  # 1-10 sustainability rating
    
    # Status
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    approval_status = Column(String, default="pending")  # pending, approved, rejected
    
    # Analytics
    view_count = Column(Integer, default=0)
    rating_average = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))
    
    # Foreign Keys
    creator_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    creator = relationship("User", back_populates="created_activities", foreign_keys=[creator_id])
    suggestions = relationship("ActivitySuggestion", back_populates="activity")
    
    def __repr__(self):
        return f"<Activity(id={self.id}, title={self.title}, category={self.category})>"
    
    @property
    def duration_formatted(self):
        if not self.duration_minutes:
            return "Durée non spécifiée"
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        if hours:
            return f"{hours}h{minutes:02d}"
        return f"{minutes}min"


class ActivitySuggestion(Base):
    """Activity suggestion model for AI-powered recommendations."""
    
    __tablename__ = "activity_suggestions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    activity_id = Column(String, ForeignKey("activities.id"), nullable=False)
    
    # Suggestion details
    suggestion_reason = Column(Text)
    confidence_score = Column(Float)  # 0.0 to 1.0
    ai_generated = Column(Boolean, default=True)
    suggestion_type = Column(String, default="automatic")  # automatic, manual, collaborative
    
    # Context
    user_context = Column(Text)  # JSON string of user context when suggestion was made
    matching_criteria = Column(Text)  # JSON string of criteria that matched
    
    # Status
    is_viewed = Column(Boolean, default=False)
    is_bookmarked = Column(Boolean, default=False)
    user_feedback = Column(String)  # positive, negative, neutral
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    viewed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="activity_suggestions")
    activity = relationship("Activity", back_populates="suggestions")
    
    def __repr__(self):
        return f"<ActivitySuggestion(id={self.id}, user_id={self.user_id}, activity_id={self.activity_id})>"