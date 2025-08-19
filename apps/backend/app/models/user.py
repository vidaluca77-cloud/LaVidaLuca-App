from sqlalchemy import Column, String, DateTime, JSON, Boolean
from datetime import datetime
import uuid
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Profile data
    skills = Column(JSON, default=list)  # List of skill tags
    availability = Column(JSON, default=list)  # List of availability options
    location = Column(String, default="")
    preferences = Column(JSON, default=list)  # List of preferred activity categories
    
    def __repr__(self):
        return f"<User(email='{self.email}', full_name='{self.full_name}')>"