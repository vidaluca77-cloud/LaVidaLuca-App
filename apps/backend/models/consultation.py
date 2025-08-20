"""
Consultation model for storing AI assistant conversations.
"""

from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


class Consultation(Base):
    """Model for storing AI assistant consultation conversations."""
    
    __tablename__ = "consultations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Conversation content
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    
    # AI metadata
    ai_model = Column(String(100), default="gpt-4")
    confidence_score = Column(String(10), nullable=True)  # Stored as string for flexibility
    tokens_used = Column(String(20), nullable=True)  # Token usage information
    
    # Conversation metadata
    category = Column(String(50), default="agriculture")  # agriculture, jardinage, permaculture, etc.
    tags = Column(JSON, default=list)  # List of relevant tags
    
    # Status and quality
    is_helpful = Column(Boolean, nullable=True)  # User feedback
    user_rating = Column(String(10), nullable=True)  # 1-5 rating if provided
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to User
    user = relationship("User", back_populates="consultations")
    
    def __repr__(self):
        return f"<Consultation(id={self.id}, user_id={self.user_id}, category={self.category})>"
    
    def to_dict(self):
        """Convert consultation to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "question": self.question,
            "answer": self.answer,
            "context": self.context,
            "ai_model": self.ai_model,
            "confidence_score": self.confidence_score,
            "tokens_used": self.tokens_used,
            "category": self.category,
            "tags": self.tags,
            "is_helpful": self.is_helpful,
            "user_rating": self.user_rating,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def to_dict_summary(self):
        """Convert consultation to dictionary with summary info only."""
        return {
            "id": str(self.id),
            "question": self.question[:100] + "..." if len(self.question) > 100 else self.question,
            "category": self.category,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_helpful": self.is_helpful,
            "user_rating": self.user_rating,
        }