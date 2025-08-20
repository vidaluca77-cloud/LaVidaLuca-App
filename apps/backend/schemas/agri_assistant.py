"""
Pydantic schemas for agricultural consultation API.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class AgriConsultationRequest(BaseModel):
    """Request schema for agricultural consultation."""
    question: str = Field(..., min_length=10, max_length=2000, description="Agricultural question or concern")
    context: Optional[str] = Field(None, max_length=1000, description="Additional context about the situation")
    category: Optional[str] = Field(None, description="Question category (soil, pests, planting, etc.)")
    session_id: Optional[str] = Field(None, description="Session ID for grouping related questions")


class AgriConsultationResponse(BaseModel):
    """Response schema for agricultural consultation."""
    id: UUID
    question: str
    answer: str
    ai_model: str
    confidence_score: Optional[float] = None
    tokens_used: int = 0
    category: Optional[str] = None
    session_id: Optional[str] = None
    created_at: datetime


class AgriConsultationHistory(BaseModel):
    """Schema for consultation history."""
    consultations: List[AgriConsultationResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool


class AgriAssistantHealthResponse(BaseModel):
    """Health check response for agricultural assistant."""
    status: str
    ai_enabled: bool
    model: str
    last_consultation: Optional[datetime] = None