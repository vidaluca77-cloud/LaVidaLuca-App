from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base
import enum


class UserRole(str, enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class ActivityCategory(str, enum.Enum):
    AGRICULTURE = "agriculture"
    ARTISANAT = "artisanat"
    ENVIRONNEMENT = "environnement"


class ActivityLevel(str, enum.Enum):
    DEBUTANT = "debutant"
    INTERMEDIAIRE = "intermediaire"
    AVANCE = "avance"


class RegistrationStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    registrations = relationship("ActivityRegistration", back_populates="user")
    created_activities = relationship("Activity", back_populates="instructor")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(Text)
    phone = Column(String)
    address = Column(Text)
    birth_date = Column(DateTime)
    mfr_location = Column(String)  # MFR (Maison Familiale Rurale) location
    interests = Column(Text)  # JSON string of interests
    experience_level = Column(Enum(ActivityLevel), default=ActivityLevel.DEBUTANT)
    profile_image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(Enum(ActivityCategory), nullable=False, index=True)
    level = Column(Enum(ActivityLevel), nullable=False)
    duration_hours = Column(Integer, nullable=False)  # Duration in hours
    max_participants = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    materials_needed = Column(Text)  # JSON string of materials
    learning_objectives = Column(Text)
    prerequisites = Column(Text)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    instructor = relationship("User", back_populates="created_activities")
    registrations = relationship("ActivityRegistration", back_populates="activity")
    sessions = relationship("ActivitySession", back_populates="activity")


class ActivitySession(Base):
    __tablename__ = "activity_sessions"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    available_spots = Column(Integer, nullable=False)
    notes = Column(Text)
    is_cancelled = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    activity = relationship("Activity", back_populates="sessions")
    registrations = relationship("ActivityRegistration", back_populates="session")


class ActivityRegistration(Base):
    __tablename__ = "activity_registrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("activity_sessions.id"), nullable=False)
    status = Column(Enum(RegistrationStatus), default=RegistrationStatus.PENDING, nullable=False)
    registration_notes = Column(Text)
    completion_notes = Column(Text)
    completion_date = Column(DateTime(timezone=True))
    rating = Column(Integer)  # 1-5 rating after completion
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="registrations")
    activity = relationship("Activity", back_populates="registrations")
    session = relationship("ActivitySession", back_populates="registrations")