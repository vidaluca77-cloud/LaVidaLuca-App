from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

# Many-to-many relationship tables
user_skills = Table('user_skills', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

activity_skills = Table('activity_skills', Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

user_activities = Table('user_activities', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('activity_id', Integer, ForeignKey('activities.id')),
    Column('completed_at', DateTime, default=func.now())
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    location = Column(String)
    availability = Column(JSON)  # Store availability as JSON array
    preferences = Column(JSON)   # Store preferences as JSON array
    is_active = Column(Boolean, default=True)
    is_student = Column(Boolean, default=False)  # MFR student status
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    skills = relationship("Skill", secondary=user_skills, back_populates="users")
    completed_activities = relationship("Activity", secondary=user_activities, back_populates="completed_by")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    category = Column(String)  # 'technical', 'soft', 'safety', etc.
    created_at = Column(DateTime, default=func.now())

    # Relationships
    users = relationship("User", secondary=user_skills, back_populates="skills")
    activities = relationship("Activity", secondary=activity_skills, back_populates="required_skills")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # 'agri', 'transfo', 'artisanat', 'nature', 'social'
    summary = Column(Text, nullable=False)
    description = Column(Text)
    duration_min = Column(Integer, nullable=False)
    seasonality = Column(JSON)  # Store as JSON array
    safety_level = Column(Integer, default=1)  # 1-5 safety complexity
    materials = Column(JSON)  # Required materials as JSON array
    location_requirements = Column(Text)
    max_participants = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    is_student_only = Column(Boolean, default=False)  # Reserved for MFR students
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    required_skills = relationship("Skill", secondary=activity_skills, back_populates="activities")
    completed_by = relationship("User", secondary=user_activities, back_populates="completed_activities")

class ActivitySession(Base):
    __tablename__ = "activity_sessions"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    duration_actual = Column(Integer)  # Actual duration in minutes
    max_participants = Column(Integer, default=10)
    location = Column(String)
    notes = Column(Text)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    created_at = Column(DateTime, default=func.now())

    # Relationships
    activity = relationship("Activity")
    instructor = relationship("User")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bio = Column(Text)
    experience_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    interests = Column(JSON)
    goals = Column(Text)
    contact_preferences = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="profile")