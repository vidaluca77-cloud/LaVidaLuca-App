"""
Activity model.
"""
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, JSON, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from ..db.base import Base


class Activity(Base):
    """Activity model."""
    
    __tablename__ = "activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    # Activity details
    duration_min = Column(Integer, nullable=False)  # Duration in minutes
    difficulty_level = Column(Integer, default=1, nullable=False)  # 1-5 scale
    safety_level = Column(Integer, default=1, nullable=False)  # 1-5 scale (1=safe, 5=risky)
    min_participants = Column(Integer, default=1, nullable=False)
    max_participants = Column(Integer, nullable=True)
    
    # Skills and requirements
    skill_tags = Column(ARRAY(String), nullable=True)  # Array of skill tags
    materials = Column(ARRAY(String), nullable=True)  # Required materials
    prerequisites = Column(ARRAY(String), nullable=True)  # Prerequisites
    
    # Location and availability
    location_type = Column(String(50), nullable=True)  # indoor, outdoor, both
    season_availability = Column(ARRAY(String), nullable=True)  # spring, summer, fall, winter
    
    # Content
    instructions = Column(Text, nullable=True)
    learning_objectives = Column(ARRAY(String), nullable=True)
    assessment_criteria = Column(Text, nullable=True)
    
    # Metadata
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Structured additional data
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    submissions = relationship("ActivitySubmission", back_populates="activity")
    creator = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self) -> str:
        return f"<Activity(id={self.id}, title={self.title})>"


class ActivitySubmission(Base):
    """Activity submission model for tracking user participation."""
    
    __tablename__ = "activity_submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    
    # Submission details
    status = Column(String(50), default="started", nullable=False)  # started, completed, submitted, reviewed
    progress_percentage = Column(Float, default=0.0, nullable=False)
    
    # Content
    submission_text = Column(Text, nullable=True)
    submission_files = Column(ARRAY(String), nullable=True)  # File paths/URLs
    
    # Assessment
    score = Column(Float, nullable=True)  # 0-100 scale
    feedback = Column(Text, nullable=True)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    
    # Structured data
    submission_data = Column(JSON, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="submissions", foreign_keys=[user_id])
    activity = relationship("Activity", back_populates="submissions")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    
    def __repr__(self) -> str:
        return f"<ActivitySubmission(id={self.id}, user_id={self.user_id}, activity_id={self.activity_id})>"