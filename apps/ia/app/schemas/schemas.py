from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from ..models.models import UserRole, ActivityCategory, ActivityLevel, RegistrationStatus


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: UserRole = UserRole.STUDENT


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# User Profile schemas
class UserProfileBase(BaseModel):
    bio: Optional[str] = Field(None, max_length=1000)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)
    birth_date: Optional[datetime] = None
    mfr_location: Optional[str] = Field(None, max_length=100)
    interests: Optional[str] = None  # JSON string
    experience_level: ActivityLevel = ActivityLevel.DEBUTANT
    profile_image_url: Optional[str] = None


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
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=2000)
    category: ActivityCategory
    level: ActivityLevel
    duration_hours: int = Field(..., ge=1, le=168)  # 1 hour to 1 week
    max_participants: int = Field(..., ge=1, le=50)
    location: str = Field(..., min_length=1, max_length=100)
    materials_needed: Optional[str] = None  # JSON string
    learning_objectives: Optional[str] = Field(None, max_length=1000)
    prerequisites: Optional[str] = Field(None, max_length=500)


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    category: Optional[ActivityCategory] = None
    level: Optional[ActivityLevel] = None
    duration_hours: Optional[int] = Field(None, ge=1, le=168)
    max_participants: Optional[int] = Field(None, ge=1, le=50)
    location: Optional[str] = Field(None, min_length=1, max_length=100)
    materials_needed: Optional[str] = None
    learning_objectives: Optional[str] = Field(None, max_length=1000)
    prerequisites: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class Activity(ActivityBase):
    id: int
    instructor_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Activity Session schemas
class ActivitySessionBase(BaseModel):
    start_date: datetime
    end_date: datetime
    available_spots: int = Field(..., ge=1, le=50)
    notes: Optional[str] = Field(None, max_length=500)

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v


class ActivitySessionCreate(ActivitySessionBase):
    activity_id: int


class ActivitySessionUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    available_spots: Optional[int] = Field(None, ge=1, le=50)
    notes: Optional[str] = Field(None, max_length=500)
    is_cancelled: Optional[bool] = None


class ActivitySession(ActivitySessionBase):
    id: int
    activity_id: int
    is_cancelled: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Activity Registration schemas
class ActivityRegistrationBase(BaseModel):
    registration_notes: Optional[str] = Field(None, max_length=500)


class ActivityRegistrationCreate(ActivityRegistrationBase):
    activity_id: int
    session_id: int


class ActivityRegistrationUpdate(BaseModel):
    status: Optional[RegistrationStatus] = None
    registration_notes: Optional[str] = Field(None, max_length=500)
    completion_notes: Optional[str] = Field(None, max_length=500)
    rating: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = Field(None, max_length=1000)


class ActivityRegistration(ActivityRegistrationBase):
    id: int
    user_id: int
    activity_id: int
    session_id: int
    status: RegistrationStatus
    completion_notes: Optional[str]
    completion_date: Optional[datetime]
    rating: Optional[int]
    feedback: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Response schemas
class Message(BaseModel):
    message: str


class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int