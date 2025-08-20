"""
Consultation schemas for request/response validation.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class ConsultationCreate(BaseModel):
    """Schema for creating a new consultation."""
    question: str = Field(..., min_length=10, max_length=2000, description="Agricultural question")
    category: Optional[str] = Field(None, max_length=100, description="Question category")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorization")
    session_id: Optional[str] = Field(None, max_length=100, description="Session identifier")
    
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty')
        return v.strip()
    
    @validator('tags')
    def validate_tags(cls, v):
        if v and len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return [tag.strip().lower() for tag in v if tag.strip()]


class ConsultationResponse(BaseModel):
    """Schema for consultation response."""
    id: str
    user_id: str
    question: str
    answer: str
    category: Optional[str]
    tags: List[str]
    ai_model: str
    response_time: Optional[str]
    confidence_score: Optional[str]
    session_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ConsultationList(BaseModel):
    """Schema for listing consultations."""
    consultations: List[ConsultationResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool


class ConsultationQuery(BaseModel):
    """Schema for consultation query parameters."""
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(20, ge=1, le=100, description="Items per page")
    category: Optional[str] = Field(None, description="Filter by category")
    session_id: Optional[str] = Field(None, description="Filter by session")
    search: Optional[str] = Field(None, min_length=3, description="Search in questions and answers")


class AIAssistantRequest(BaseModel):
    """Schema for AI assistant request."""
    question: str = Field(..., min_length=10, max_length=2000)
    context: Optional[str] = Field(None, max_length=1000, description="Additional context")
    
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty')
        return v.strip()


class AIAssistantResponse(BaseModel):
    """Schema for AI assistant response."""
    answer: str
    category: Optional[str]
    tags: List[str]
    response_time: str
    confidence_score: Optional[str]
    consultation_id: str