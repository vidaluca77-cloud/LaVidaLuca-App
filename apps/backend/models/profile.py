"""
Profile model for user profile management - separate from User for enhanced structure.
"""

from sqlalchemy import Column, String, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


class Profile(Base):
    """User profile model with skills, availability, location, and preferences."""
    
    __tablename__ = "profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    
    # Core profile information
    skills = Column(ARRAY(String), default=list)  # e.g., ["agriculture", "menuiserie", "cuisine"]
    availability = Column(ARRAY(String), default=list)  # e.g., ["weekdays", "evenings", "weekends"]
    location = Column(String(255))  # Physical location or region
    preferences = Column(ARRAY(String), default=list)  # Learning preferences, interests
    
    # Experience and education
    experience_level = Column(String(50), default="beginner")  # beginner, intermediate, advanced
    education_background = Column(ARRAY(String), default=list)  # Educational domains
    certifications = Column(ARRAY(String), default=list)  # Certifications held
    
    # Learning preferences
    learning_style = Column(ARRAY(String), default=list)  # visual, auditory, kinesthetic, reading
    preferred_activity_types = Column(ARRAY(String), default=list)  # outdoor, workshop, theory, practice
    preferred_group_size = Column(String(20))  # individual, small_group, large_group
    
    # Availability details
    time_availability = Column(JSON, default=dict)  # Detailed availability schedule
    seasonal_availability = Column(ARRAY(String), default=list)  # spring, summer, autumn, winter
    
    # Interests and goals
    interests = Column(ARRAY(String), default=list)  # Specific interests/hobbies
    learning_goals = Column(ARRAY(String), default=list)  # What they want to achieve
    career_goals = Column(ARRAY(String), default=list)  # Career aspirations
    
    # Safety and accessibility
    physical_limitations = Column(ARRAY(String), default=list)  # Any physical constraints
    safety_preferences = Column(JSON, default=dict)  # Safety level preferences
    accessibility_needs = Column(ARRAY(String), default=list)  # Special accessibility requirements
    
    # Social preferences
    mentoring_interest = Column(Boolean, default=False)  # Interested in mentoring others
    collaboration_preference = Column(String(20), default="flexible")  # solo, team, flexible
    communication_style = Column(ARRAY(String), default=list)  # direct, supportive, structured
    
    # Geographic and logistics
    travel_willingness = Column(String(20), default="local")  # local, regional, national
    transportation_access = Column(ARRAY(String), default=list)  # car, public_transport, bicycle
    
    # Additional flexible data
    custom_fields = Column(JSON, default=dict)  # For future extensibility
    
    # Profile completion and settings
    is_complete = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)  # Whether profile is visible to others
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<Profile(id={self.id}, user_id={self.user_id}, location={self.location})>"
    
    def to_dict(self):
        """Convert profile to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "skills": self.skills or [],
            "availability": self.availability or [],
            "location": self.location,
            "preferences": self.preferences or [],
            "experience_level": self.experience_level,
            "education_background": self.education_background or [],
            "certifications": self.certifications or [],
            "learning_style": self.learning_style or [],
            "preferred_activity_types": self.preferred_activity_types or [],
            "preferred_group_size": self.preferred_group_size,
            "time_availability": self.time_availability or {},
            "seasonal_availability": self.seasonal_availability or [],
            "interests": self.interests or [],
            "learning_goals": self.learning_goals or [],
            "career_goals": self.career_goals or [],
            "physical_limitations": self.physical_limitations or [],
            "safety_preferences": self.safety_preferences or {},
            "accessibility_needs": self.accessibility_needs or [],
            "mentoring_interest": self.mentoring_interest,
            "collaboration_preference": self.collaboration_preference,
            "communication_style": self.communication_style or [],
            "travel_willingness": self.travel_willingness,
            "transportation_access": self.transportation_access or [],
            "custom_fields": self.custom_fields or {},
            "is_complete": self.is_complete,
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @property
    def completion_percentage(self) -> float:
        """Calculate profile completion percentage."""
        total_fields = 15  # Key fields to consider for completion
        completed_fields = 0
        
        if self.skills:
            completed_fields += 1
        if self.availability:
            completed_fields += 1
        if self.location:
            completed_fields += 1
        if self.preferences:
            completed_fields += 1
        if self.experience_level != "beginner":
            completed_fields += 1
        if self.education_background:
            completed_fields += 1
        if self.learning_style:
            completed_fields += 1
        if self.preferred_activity_types:
            completed_fields += 1
        if self.interests:
            completed_fields += 1
        if self.learning_goals:
            completed_fields += 1
        if self.career_goals:
            completed_fields += 1
        if self.collaboration_preference != "flexible":
            completed_fields += 1
        if self.travel_willingness != "local":
            completed_fields += 1
        if self.transportation_access:
            completed_fields += 1
        if self.time_availability:
            completed_fields += 1
            
        return round((completed_fields / total_fields) * 100, 1)