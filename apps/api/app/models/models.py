from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Profile information
    bio = Column(Text)
    location = Column(String)
    phone = Column(String)
    birth_date = Column(DateTime)
    skills = Column(JSON)  # List of skill tags
    preferences = Column(JSON)  # User preferences for activities
    availability = Column(JSON)  # Available time slots
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    participations = relationship("Participation", back_populates="user")
    progress_records = relationship("Progress", back_populates="user")


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text)
    
    # Activity metadata
    duration_min = Column(Integer, nullable=False)
    skill_tags = Column(JSON)  # Required/taught skills
    seasonality = Column(JSON)  # When activity is available
    safety_level = Column(Integer, default=1)  # 1-3 safety level
    materials = Column(JSON)  # Required materials/equipment
    max_participants = Column(Integer, default=10)
    min_age = Column(Integer, default=16)
    
    # Location and logistics
    location = Column(String)
    difficulty_level = Column(Integer, default=1)  # 1-5
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    participations = relationship("Participation", back_populates="activity")


class Participation(Base):
    __tablename__ = "participations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    
    # Participation details
    status = Column(String, default="registered")  # registered, confirmed, completed, cancelled
    scheduled_date = Column(DateTime)
    completion_date = Column(DateTime)
    
    # Feedback
    rating = Column(Integer)  # 1-5 stars
    comment = Column(Text)
    feedback = Column(JSON)  # Structured feedback
    
    # Progress tracking
    skills_acquired = Column(JSON)  # Skills learned/improved
    completion_percentage = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="participations")
    activity = relationship("Activity", back_populates="participations")
    progress_records = relationship("Progress", back_populates="participation")


class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    participation_id = Column(Integer, ForeignKey("participations.id"), nullable=True)
    
    # Progress data
    metric_type = Column(String, nullable=False)  # skill_improvement, activity_completion, etc.
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String)  # %, hours, level, etc.
    
    # Context
    description = Column(Text)
    evidence = Column(JSON)  # Photos, documents, etc.
    verified_by = Column(String)  # Who verified this progress
    
    # Metadata
    recorded_date = Column(DateTime, default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress_records")
    participation = relationship("Participation", back_populates="progress_records")