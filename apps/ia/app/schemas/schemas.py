from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class ActivityBase(BaseModel):
    slug: str
    title: str
    category: str
    summary: str
    duration_min: int
    skill_tags: List[str]
    seasonality: List[str]
    safety_level: int
    materials: List[str]

class ActivityCreate(ActivityBase):
    id: str

class ActivityResponse(ActivityBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserProfileBase(BaseModel):
    skills: List[str]
    availability: List[str]
    location: str
    preferences: List[str]

class UserProfileCreate(UserProfileBase):
    user_id: str

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ContactSubmissionBase(BaseModel):
    name: str
    email: EmailStr
    message: str
    type: str = "contact"

class ContactSubmissionCreate(ContactSubmissionBase):
    pass

class ContactSubmissionResponse(ContactSubmissionBase):
    id: int
    status: str
    created_at: datetime
    processed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class SuggestionResponse(BaseModel):
    activity: ActivityResponse
    score: int
    reasons: List[str]

class MatchingRequest(BaseModel):
    profile: UserProfileBase

class MatchingResponse(BaseModel):
    suggestions: List[SuggestionResponse]