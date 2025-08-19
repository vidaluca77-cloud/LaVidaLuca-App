from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from ..core.database import Base


class ActivityCategory(str, Enum):
    """Categories for activities as mentioned in the project context"""
    AGRICULTURE = "agriculture"
    ARTISANAT = "artisanat"
    ENVIRONNEMENT = "environnement"
    FORMATION = "formation"
    INNOVATION = "innovation"


class ActivityDifficulty(str, Enum):
    """Difficulty levels for activities"""
    DEBUTANT = "debutant"
    INTERMEDIAIRE = "intermediaire"
    AVANCE = "avance"


class Activity(Base):
    """Activity model for the 30 MFR activities catalog"""
    
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(ActivityCategory), nullable=False, index=True)
    difficulty = Column(SQLEnum(ActivityDifficulty), nullable=False)
    
    # Activity details
    duration_hours = Column(Integer, nullable=True)  # Estimated duration in hours
    materials_needed = Column(Text, nullable=True)   # JSON or text list of materials
    prerequisites = Column(Text, nullable=True)      # Prerequisites for the activity
    learning_objectives = Column(Text, nullable=True) # What students will learn
    
    # Location and logistics
    location_type = Column(String(100), nullable=True)  # indoor, outdoor, field, workshop
    max_participants = Column(Integer, nullable=True)
    
    # Status and availability
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Creator (MFR instructor or admin)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="created_activities")
    
    def __repr__(self):
        return f"<Activity(id={self.id}, title='{self.title}', category='{self.category}')>"


# Add back-reference to User model
from .user import User
User.created_activities = relationship("Activity", back_populates="creator")