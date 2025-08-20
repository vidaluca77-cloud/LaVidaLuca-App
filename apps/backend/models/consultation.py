"""
Consultation model for agricultural AI assistant Q&A sessions.
"""

from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class Consultation(Base):
    """Consultation model for agricultural AI assistant."""
    
    __tablename__ = "consultations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Question and answer content
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    
    # Context and metadata
    category = Column(String(100))  # e.g., "permaculture", "crop_management", "animal_health"
    tags = Column(JSON, default=list)  # Flexible tagging system
    
    # AI response metadata
    ai_model = Column(String(50), default="gpt-3.5-turbo")
    response_time = Column(String(20))  # Time taken to generate response
    confidence_score = Column(String(10))  # Optional confidence indicator
    
    # Session tracking
    session_id = Column(String(100))  # To group related questions in a session
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
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
            "category": self.category,
            "tags": self.tags,
            "ai_model": self.ai_model,
            "response_time": self.response_time,
            "confidence_score": self.confidence_score,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }