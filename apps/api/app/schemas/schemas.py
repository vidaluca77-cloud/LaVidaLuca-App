from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Union
from datetime import datetime
from enum import Enum

class ActivityCategory(str, Enum):
    AGRI = "agri"
    TRANSFO = "transfo"
    ARTISANAT = "artisanat"
    NATURE = "nature"
    SOCIAL = "social"

class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class RegistrationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class SessionStatus(str, Enum):
    OPEN = "open"
    FULL = "full"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    is_mfr_student: bool = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    is_mfr_student: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

# User Profile schemas
class UserProfileBase(BaseModel):
    bio: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    birth_date: Optional[datetime] = None
    emergency_contact: Optional[str] = Field(None, max_length=255)
    medical_info: Optional[str] = None
    experience_level: ExperienceLevel = ExperienceLevel.BEGINNER
    skills: List[str] = []
    availability: List[str] = []
    preferences: List[ActivityCategory] = []

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Activity schemas
class ActivityBase(BaseModel):
    title: str = Field(..., max_length=255)
    category: ActivityCategory
    summary: str
    description: Optional[str] = None
    duration_min: int = Field(..., gt=0, le=480)  # Max 8 hours
    safety_level: int = Field(default=1, ge=1, le=3)
    max_participants: int = Field(default=10, gt=0, le=50)
    min_age: int = Field(default=14, ge=10, le=25)
    requires_mfr: bool = False
    skill_tags: List[str] = []
    seasonality: List[str] = []
    materials: List[str] = []

class ActivityCreate(ActivityBase):
    slug: str = Field(..., max_length=100)

class ActivityUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_min: Optional[int] = Field(None, gt=0, le=480)
    safety_level: Optional[int] = Field(None, ge=1, le=3)
    max_participants: Optional[int] = Field(None, gt=0, le=50)
    min_age: Optional[int] = Field(None, ge=10, le=25)
    requires_mfr: Optional[bool] = None
    skill_tags: Optional[List[str]] = None
    seasonality: Optional[List[str]] = None
    materials: Optional[List[str]] = None
    is_active: Optional[bool] = None

class Activity(ActivityBase):
    id: int
    slug: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Activity Session schemas
class ActivitySessionBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    location: str = Field(..., max_length=255)
    instructor: Optional[str] = Field(None, max_length=100)
    max_participants: int = Field(default=10, gt=0, le=50)

class ActivitySessionCreate(ActivitySessionBase):
    activity_id: int

class ActivitySessionUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=255)
    instructor: Optional[str] = Field(None, max_length=100)
    max_participants: Optional[int] = Field(None, gt=0, le=50)
    status: Optional[SessionStatus] = None

class ActivitySession(ActivitySessionBase):
    id: int
    activity_id: int
    current_participants: int
    status: SessionStatus
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Registration schemas
class ActivityRegistrationBase(BaseModel):
    notes: Optional[str] = None

class ActivityRegistrationCreate(ActivityRegistrationBase):
    activity_id: int
    session_id: Optional[int] = None

class ActivityRegistrationUpdate(BaseModel):
    status: Optional[RegistrationStatus] = None
    notes: Optional[str] = None

class ActivityRegistration(ActivityRegistrationBase):
    id: int
    user_id: int
    activity_id: int
    session_id: Optional[int]
    status: RegistrationStatus
    registration_date: datetime
    
    # Include related objects
    activity: Optional[Activity] = None
    session: Optional[ActivitySession] = None
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username_or_email: str
    password: str

# Response schemas
class UserWithProfile(User):
    profile: Optional[UserProfile] = None

class ActivityWithSessions(Activity):
    sessions: List[ActivitySession] = []

class RegistrationWithDetails(ActivityRegistration):
    user: Optional[User] = None
    activity: Optional[Activity] = None
    session: Optional[ActivitySession] = None