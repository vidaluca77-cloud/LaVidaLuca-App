"""
Consultation model for agricultural AI assistant.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base


class Consultation(Base):
    """Consultation model for agricultural AI assistant."""
    
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Optional for anonymous users
    
    # Consultation content
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    
    # Additional context
    context = Column(JSON, default=dict)  # Store additional context like crop type, region, etc.
    
    # AI model metadata
    model_used = Column(String, default="gpt-3.5-turbo")
    tokens_used = Column(Integer)  # Store token usage for analytics
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to User (if authenticated)
    user = relationship("User")
    
    def __repr__(self):
        return f"<Consultation(id={self.id}, user_id={self.user_id})>"
    
    def to_dict(self):
        """Convert consultation to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "question": self.question,
            "response": self.response,
            "context": self.context,
            "model_used": self.model_used,
            "tokens_used": self.tokens_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }