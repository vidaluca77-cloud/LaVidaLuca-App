from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    Float, JSON, ForeignKey, Table, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

Base = declarative_base()

# Enums
class UserRole(str, enum.Enum):
    STUDENT = "student"  # Élève MFR
    MENTOR = "mentor"    # Encadrant/formateur
    ADMIN = "admin"      # Administrateur
    VISITOR = "visitor"  # Visiteur

class ActivityCategory(str, enum.Enum):
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"

class ReservationStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class SafetyLevel(int, enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Association tables for many-to-many relationships
user_skills = Table(
    'user_skills',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('skill_name', String(50))
)

activity_skills = Table(
    'activity_skills',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id')),
    Column('skill_name', String(50))
)

activity_materials = Table(
    'activity_materials',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id')),
    Column('material_name', String(100))
)

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.VISITOR)
    
    # Profile information
    location = Column(String(255))
    phone = Column(String(20))
    bio = Column(Text)
    availability = Column(JSON)  # ["weekend", "semaine", "matin", etc.]
    preferences = Column(JSON)   # ["agri", "nature", etc.]
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    reservations = relationship("Reservation", back_populates="user")
    evaluations = relationship("Evaluation", back_populates="user")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    address = Column(Text)
    departement = Column(String(100))
    coordinates = Column(JSON)  # {"lat": x, "lng": y}
    contact_person = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    
    # Capacities and features
    max_capacity = Column(Integer, default=10)
    facilities = Column(JSON)  # ["parking", "sanitaires", etc.]
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    activities = relationship("Activity", back_populates="location")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(Enum(ActivityCategory), nullable=False)
    summary = Column(Text)
    description = Column(Text)
    
    # Duration and scheduling
    duration_min = Column(Integer, nullable=False)
    seasonality = Column(JSON)  # ["printemps", "ete", "automne", "hiver", "toutes"]
    
    # Safety and requirements
    safety_level = Column(Enum(SafetyLevel), default=SafetyLevel.LOW)
    min_age = Column(Integer, default=16)
    max_participants = Column(Integer, default=8)
    
    # Requirements and materials (many-to-many via association tables)
    prerequisites = Column(Text)
    
    # Location
    location_id = Column(Integer, ForeignKey("locations.id"))
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    location = relationship("Location", back_populates="activities")
    reservations = relationship("Reservation", back_populates="activity")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    
    # Scheduling
    scheduled_date = Column(DateTime(timezone=True))
    duration_actual = Column(Integer)  # Actual duration in minutes
    
    # Status and management
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)
    notes = Column(Text)
    mentor_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reservations")
    activity = relationship("Activity", back_populates="reservations")
    evaluation = relationship("Evaluation", back_populates="reservation", uselist=False)

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Evaluation scores (1-5 scale)
    skill_demonstration = Column(Float)
    safety_compliance = Column(Float)
    teamwork = Column(Float)
    initiative = Column(Float)
    overall_rating = Column(Float)
    
    # Comments
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    mentor_comments = Column(Text)
    student_feedback = Column(Text)
    
    # Progress tracking
    goals_achieved = Column(JSON)  # List of achieved goals
    next_recommendations = Column(JSON)  # Recommended next activities
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    reservation = relationship("Reservation", back_populates="evaluation")
    user = relationship("User", back_populates="evaluations")