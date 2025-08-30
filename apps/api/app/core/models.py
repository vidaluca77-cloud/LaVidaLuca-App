from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# Association table for user skills (many-to-many)
user_skills = Table(
    'user_skills',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('skill_name', String(50), primary_key=True)
)

# Association table for user availability (many-to-many)
user_availability = Table(
    'user_availability', 
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('availability_type', String(20), primary_key=True)
)

# Association table for user category preferences (many-to-many)
user_preferences = Table(
    'user_preferences',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('category', String(20), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_mfr_student = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    registrations = relationship("ActivityRegistration", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    bio = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    birth_date = Column(DateTime, nullable=True)
    emergency_contact = Column(String(255), nullable=True)
    medical_info = Column(Text, nullable=True)
    experience_level = Column(String(20), default="beginner")  # beginner, intermediate, advanced
    
    # JSON fields for flexibility
    skills = Column(JSON, default=list)  # List of skill names
    availability = Column(JSON, default=list)  # List of availability types
    preferences = Column(JSON, default=list)  # List of preferred categories
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(20), nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    duration_min = Column(Integer, nullable=False)
    safety_level = Column(Integer, default=1)  # 1-3, 1 = low risk
    max_participants = Column(Integer, default=10)
    min_age = Column(Integer, default=14)
    is_active = Column(Boolean, default=True)
    requires_mfr = Column(Boolean, default=False)  # Only for MFR students
    
    # JSON fields
    skill_tags = Column(JSON, default=list)  # Required skills
    seasonality = Column(JSON, default=list)  # Available seasons
    materials = Column(JSON, default=list)  # Required materials
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    registrations = relationship("ActivityRegistration", back_populates="activity")
    sessions = relationship("ActivitySession", back_populates="activity")

class ActivitySession(Base):
    __tablename__ = "activity_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    instructor = Column(String(100), nullable=True)
    max_participants = Column(Integer, default=10)
    current_participants = Column(Integer, default=0)
    status = Column(String(20), default="open")  # open, full, cancelled, completed
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    activity = relationship("Activity", back_populates="sessions")
    registrations = relationship("ActivityRegistration", back_populates="session")

class ActivityRegistration(Base):
    __tablename__ = "activity_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    session_id = Column(Integer, ForeignKey("activity_sessions.id"), nullable=True)
    status = Column(String(20), default="pending")  # pending, confirmed, cancelled, completed
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="registrations")
    activity = relationship("Activity", back_populates="registrations")
    session = relationship("ActivitySession", back_populates="registrations")