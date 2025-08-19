from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Table d'association pour les compétences utilisateur
user_skills = Table(
    'user_skills',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('skill_name', String, primary_key=True)
)

# Table d'association pour les préférences utilisateur
user_preferences = Table(
    'user_preferences', 
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('category', String, primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_mfr_student = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    recommendations = relationship("Recommendation", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    location = Column(String)
    availability = Column(ARRAY(String))  # ['weekend', 'semaine', 'matin', etc.]
    experience_level = Column(String, default="debutant")  # debutant, intermediaire, avance
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="profile")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # agri, transfo, artisanat, nature, social
    summary = Column(Text)
    description = Column(Text)
    duration_min = Column(Integer)
    skill_tags = Column(ARRAY(String))
    seasonality = Column(ARRAY(String))
    safety_level = Column(Integer)  # 1-3, 1=sûr, 3=attention requise
    materials = Column(ARRAY(String))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    recommendations = relationship("Recommendation", back_populates="activity")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    score = Column(Float)
    reasons = Column(ARRAY(String))
    ai_explanation = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", back_populates="recommendations")
    activity = relationship("Activity", back_populates="recommendations")