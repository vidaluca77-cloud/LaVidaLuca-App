from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

# Association table for user skills (many-to-many)
user_skills = Table(
    'user_skills',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('skill_name', String, ForeignKey('skills.name'))
)

# Association table for user activity preferences (many-to-many)
user_activity_preferences = Table(
    'user_activity_preferences',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)

class CategoryEnum(enum.Enum):
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Profile fields based on frontend UserProfile interface
    availability = Column(Text, nullable=True)  # JSON string of availability options
    preferences = Column(Text, nullable=True)   # JSON string of category preferences
    
    # Relationships
    skills = relationship("Skill", secondary=user_skills, back_populates="users")
    preferred_activities = relationship("Activity", secondary=user_activity_preferences, back_populates="interested_users")
    suggestions = relationship("ActivitySuggestion", back_populates="user")

class Skill(Base):
    __tablename__ = "skills"
    
    name = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    
    # Relationships
    users = relationship("User", secondary=user_skills, back_populates="skills")
    activities = relationship("Activity", secondary="activity_skills", back_populates="required_skills")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)  # Longer description
    duration_min = Column(Integer, nullable=False)
    safety_level = Column(Integer, default=1)  # 1-3 safety level
    seasonality = Column(Text, nullable=True)  # JSON string of seasons
    materials = Column(Text, nullable=True)    # JSON string of required materials
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    required_skills = relationship("Skill", secondary="activity_skills", back_populates="activities")
    interested_users = relationship("User", secondary=user_activity_preferences, back_populates="preferred_activities")
    suggestions = relationship("ActivitySuggestion", back_populates="activity")

# Association table for activity skills
activity_skills = Table(
    'activity_skills',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id')),
    Column('skill_name', String, ForeignKey('skills.name'))
)

class ActivitySuggestion(Base):
    __tablename__ = "activity_suggestions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    score = Column(Float, nullable=False)
    reasons = Column(Text, nullable=True)  # JSON string of reasons
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="suggestions")
    activity = relationship("Activity", back_populates="suggestions")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())