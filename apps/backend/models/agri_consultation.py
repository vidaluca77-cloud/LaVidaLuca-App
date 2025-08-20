"""
Agricultural consultation model for AI-powered farming assistance.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


class AgriConsultation(Base):
    """Model for storing agricultural consultation sessions with AI assistant."""
    
    __tablename__ = "agri_consultations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User relationship (optional for anonymous users)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Consultation content
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    
    # AI metadata
    ai_model = Column(String(100), default="gpt-3.5-turbo")
    confidence_score = Column(Float, nullable=True)
    tokens_used = Column(Integer, default=0)
    
    # Category classification
    category = Column(String(100), nullable=True)  # e.g., "soil", "pests", "planting", etc.
    
    # Session tracking
    session_id = Column(String(255), nullable=True)  # For grouping related questions
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to user (if authenticated)
    user = relationship("User", back_populates="agri_consultations")
    
    def __repr__(self):
        return f"<AgriConsultation(id={self.id}, category={self.category})>"
    
    def to_dict(self):
        """Convert consultation to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "question": self.question,
            "answer": self.answer,
            "ai_model": self.ai_model,
            "confidence_score": self.confidence_score,
            "tokens_used": self.tokens_used,
            "category": self.category,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }