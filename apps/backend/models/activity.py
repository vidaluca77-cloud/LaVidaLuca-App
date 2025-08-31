"""
Activity model for educational activities and learning experiences.
"""

from sqlalchemy import Column, String, Text, Integer, Float, JSON, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid

from ..database import Base


class Activity(Base):
    """Activity model for educational activities."""

    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic information
    title = Column(String(255), nullable=False)
    category = Column(
        String(50), nullable=False
    )  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text)

    # Activity details
    duration_min = Column(Integer, nullable=False)  # Duration in minutes
    skill_tags = Column(ARRAY(String), default=list)  # Skills/competencies
    safety_level = Column(Integer, default=1)  # 1=very safe, 5=risky
    materials = Column(ARRAY(String), default=list)  # Required materials

    # Difficulty and requirements
    difficulty_level = Column(Integer, default=1)  # 1=beginner, 5=expert
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
    created_by = Column(UUID(as_uuid=True))  # Reference to user who created
    is_published = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)

    # Search and categorization
    keywords = Column(ARRAY(String), default=list)
    season_tags = Column(ARRAY(String), default=list)  # spring, summer, autumn, winter

    # Additional data
    external_resources = Column(JSON, default=dict)  # Links, references
    metadata = Column(JSON, default=dict)  # Flexible additional data

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Activity(id={self.id}, title={self.title}, category={self.category})>"

    def to_dict(self):
        """Convert activity to dictionary."""
        return {
            "id": str(self.id),
            "title": self.title,
            "category": self.category,
            "summary": self.summary,
            "description": self.description,
            "duration_min": self.duration_min,
            "skill_tags": self.skill_tags or [],
            "safety_level": self.safety_level,
            "materials": self.materials or [],
            "difficulty_level": self.difficulty_level,
            "min_participants": self.min_participants,
            "max_participants": self.max_participants,
            "age_min": self.age_min,
            "age_max": self.age_max,
            "location_type": self.location_type,
            "location_details": self.location_details,
            "preparation_time": self.preparation_time,
            "learning_objectives": self.learning_objectives or [],
            "assessment_methods": self.assessment_methods or [],
            "pedagogical_notes": self.pedagogical_notes,
            "is_published": self.is_published,
            "is_featured": self.is_featured,
            "keywords": self.keywords or [],
            "season_tags": self.season_tags or [],
            "external_resources": self.external_resources or {},
            "metadata": self.metadata or {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
