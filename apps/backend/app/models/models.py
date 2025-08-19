from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base


class User(Base):
    """Enhanced User model with profile support."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    
    # Enhanced profile fields
    profile = Column(JSON, default=dict)  # Flexible profile data
    
    # User status
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relationships
    activities = relationship("Activity", back_populates="creator")
    suggestions = relationship("ActivitySuggestion", back_populates="user")


class Activity(Base):
    """Enhanced Activity model with comprehensive fields."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)  # agri, transfo, artisanat, nature, social
    
    # Learning details
    difficulty_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    duration_minutes = Column(Integer)
    location = Column(String)
    equipment_needed = Column(Text)
    learning_objectives = Column(Text)
    
    # Enhanced fields
    skill_tags = Column(JSON, default=list)  # Skills/competencies required
    materials = Column(JSON, default=list)  # Required materials list
    safety_level = Column(Integer, default=1)  # 1=very safe, 5=risky
    min_participants = Column(Integer, default=1)
    max_participants = Column(Integer)
    age_min = Column(Integer)
    age_max = Column(Integer)
    
    # Seasonal and location info
    season_tags = Column(JSON, default=list)  # spring, summer, autumn, winter
    location_type = Column(String)  # indoor, outdoor, field, workshop
    preparation_time = Column(Integer, default=0)  # Preparation time in minutes
    
    # Educational metadata
    assessment_methods = Column(JSON, default=list)
    pedagogical_notes = Column(Text)
    keywords = Column(JSON, default=list)
    external_resources = Column(JSON, default=dict)  # Links, references
    
    # Status and visibility
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    creator_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    creator = relationship("User", back_populates="activities")
    suggestions = relationship("ActivitySuggestion", back_populates="activity")

    def to_dict(self):
        """Convert activity to dictionary for API responses."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "difficulty_level": self.difficulty_level,
            "duration_minutes": self.duration_minutes,
            "location": self.location,
            "equipment_needed": self.equipment_needed,
            "learning_objectives": self.learning_objectives,
            "skill_tags": self.skill_tags or [],
            "materials": self.materials or [],
            "safety_level": self.safety_level,
            "min_participants": self.min_participants,
            "max_participants": self.max_participants,
            "age_min": self.age_min,
            "age_max": self.age_max,
            "season_tags": self.season_tags or [],
            "location_type": self.location_type,
            "preparation_time": self.preparation_time,
            "assessment_methods": self.assessment_methods or [],
            "pedagogical_notes": self.pedagogical_notes,
            "keywords": self.keywords or [],
            "external_resources": self.external_resources or {},
            "is_published": self.is_published,
            "is_featured": self.is_featured,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "creator_id": self.creator_id,
        }


class ActivitySuggestion(Base):
    """Activity suggestion model for AI recommendations."""
    __tablename__ = "activity_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    
    # Suggestion metadata
    suggestion_reason = Column(Text)
    score = Column(Integer, default=50)  # Suggestion confidence score 0-100
    ai_generated = Column(Boolean, default=True)
    
    # Suggestion context
    user_query = Column(Text)  # Original user query that led to this suggestion
    matching_criteria = Column(JSON, default=dict)  # What criteria matched
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="suggestions")
    activity = relationship("Activity", back_populates="suggestions")


class Contact(Base):
    """Contact form submissions and communications."""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Contact information
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    organization = Column(String)
    
    # Message details
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    contact_type = Column(String, default="general")  # general, partnership, support, etc.
    
    # Status tracking
    status = Column(String, default="new")  # new, in_progress, resolved, closed
    priority = Column(String, default="normal")  # low, normal, high, urgent
    assigned_to = Column(Integer, ForeignKey("users.id"))
    
    # Response tracking
    is_responded = Column(Boolean, default=False)
    response_count = Column(Integer, default=0)
    last_response_at = Column(DateTime(timezone=True))
    
    # Additional metadata
    extra_data = Column(JSON, default=dict)  # Flexible additional data
    tags = Column(JSON, default=list)  # Tags for categorization
    
    # Privacy and consent
    consent_privacy = Column(Boolean, default=True)
    consent_marketing = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    assigned_user = relationship("User")