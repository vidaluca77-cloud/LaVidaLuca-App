from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Profil utilisateur basé sur UserProfile du frontend
    skills = Column(ARRAY(String), default=[])
    availability = Column(ARRAY(String), default=[])
    location = Column(String, nullable=True)
    preferences = Column(ARRAY(String), default=[])
    
    # Métadonnées
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())