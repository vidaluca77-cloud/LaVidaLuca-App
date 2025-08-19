"""Progress model."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.session import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .activity import Activity  # noqa: F401


class Progress(Base):
    """Progress tracking model."""
    
    __tablename__ = "progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    completed_at = Column(DateTime, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 rating
    feedback = Column(Text, nullable=True)
    skills_gained = Column(ARRAY(String), nullable=False, default=[])
    instructor_notes = Column(Text, nullable=True)
    time_spent_minutes = Column(Integer, nullable=True)
    achievements = Column(ARRAY(String), nullable=False, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress_records")
    activity = relationship("Activity", back_populates="progress_records")