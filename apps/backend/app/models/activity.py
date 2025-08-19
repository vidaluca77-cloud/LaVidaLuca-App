"""
Activity model for La Vida Luca application.
"""

from sqlalchemy import Column, Integer, String, Text, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import enum

from app.core.database import Base


class ActivityCategory(str, enum.Enum):
    """
    Enumeration for activity categories.
    """
    AGRI = "agri"  # Agriculture - élevage, cultures, soins aux animaux
    TRANSFO = "transfo"  # Transformation - fromage, conserves, pain
    ARTISANAT = "artisanat"  # Artisanat - menuiserie, construction, réparation
    NATURE = "nature"  # Environnement - plantation, compostage, écologie
    SOCIAL = "social"  # Animation - accueil, visites, ateliers enfants


class Activity(Base):
    """
    Activity model for storing agricultural and educational activities.
    """
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(Enum(ActivityCategory), nullable=False)
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)  # Extended description
    
    # Activity specifications
    duration_min = Column(Integer, nullable=False)  # Duration in minutes
    skill_tags = Column(JSON, default=list)  # Required/developed skills
    seasonality = Column(JSON, default=list)  # Seasonal availability
    safety_level = Column(Integer, default=1)  # Safety level 1-3
    materials = Column(JSON, default=list)  # Required materials/equipment
    
    # Additional metadata
    min_participants = Column(Integer, default=1)
    max_participants = Column(Integer, default=10)
    location_type = Column(String(100), nullable=True)  # indoor/outdoor/both
    difficulty_level = Column(Integer, default=1)  # Difficulty 1-5
    
    # Educational information
    learning_objectives = Column(JSON, default=list)
    prerequisites = Column(JSON, default=list)
    
    # Status and metadata
    is_active = Column(Integer, default=1)  # Using Integer for SQLite compatibility
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Activity(id={self.id}, slug='{self.slug}', title='{self.title}', category='{self.category.value}')>"