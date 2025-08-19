from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Association table for user-activity registrations
user_activity_registration = Table(
    'user_activity_registrations',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True),
    Column('registered_at', DateTime(timezone=True), server_default=func.now())
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    skills = Column(JSON, default=list)
    availability = Column(JSON, default=list)
    location = Column(String, nullable=True)
    preferences = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to registered activities
    registered_activities = relationship(
        "Activity",
        secondary=user_activity_registration,
        back_populates="registered_users"
    )


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # 'agri', 'transfo', 'artisanat', 'nature', 'social'
    summary = Column(Text, nullable=True)
    duration_min = Column(Integer, nullable=False)
    skill_tags = Column(JSON, default=list)
    seasonality = Column(JSON, default=list)
    safety_level = Column(Integer, default=1)
    materials = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to registered users
    registered_users = relationship(
        "User",
        secondary=user_activity_registration,
        back_populates="registered_activities"
    )