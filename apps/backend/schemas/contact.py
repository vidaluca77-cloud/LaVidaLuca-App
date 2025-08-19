"""
Contact schemas for contact form submissions and communications.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, UUID4
from enum import Enum


class ContactType(str, Enum):
    """Contact request types."""
    GENERAL = "general"
    PARTNERSHIP = "partnership"
    SUPPORT = "support"
    FEEDBACK = "feedback"
    COLLABORATION = "collaboration"
    PRESS = "press"


class ContactStatus(str, Enum):
    """Contact status options."""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ContactPriority(str, Enum):
    """Contact priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class ContactBase(BaseModel):
    """Base contact schema."""
    name: str = Field(..., max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    organization: Optional[str] = Field(None, max_length=255)
    subject: str = Field(..., max_length=500)
    message: str = Field(..., min_length=10)
    contact_type: ContactType = ContactType.GENERAL


class ContactCreate(ContactBase):
    """Contact creation schema."""
    consent_privacy: bool = True
    consent_marketing: bool = False
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Jean Dupont",
                "email": "jean.dupont@example.com",
                "phone": "+33123456789",
                "organization": "MFR de Provence",
                "subject": "Demande de partenariat",
                "message": "Bonjour, nous souhaitons explorer une collaboration avec La Vida Luca pour nos formations...",
                "contact_type": "partnership",
                "consent_privacy": True,
                "consent_marketing": False
            }
        }


class ContactUpdate(BaseModel):
    """Contact update schema (for admins)."""
    status: Optional[ContactStatus] = None
    priority: Optional[ContactPriority] = None
    assigned_to: Optional[UUID4] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class ContactResponse(BaseModel):
    """Contact response schema."""
    id: UUID4
    name: str
    email: EmailStr
    phone: Optional[str]
    organization: Optional[str]
    subject: str
    message: str
    contact_type: str
    status: str
    priority: str
    assigned_to: Optional[UUID4]
    is_responded: bool
    response_count: int
    last_response_at: Optional[datetime]
    metadata: Dict[str, Any]
    tags: List[str]
    consent_privacy: bool
    consent_marketing: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ContactListResponse(BaseModel):
    """Contact list response schema (minimal info for listings)."""
    id: UUID4
    name: str
    email: EmailStr
    subject: str
    contact_type: str
    status: str
    priority: str
    is_responded: bool
    created_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ContactFilters(BaseModel):
    """Contact search and filter parameters."""
    contact_type: Optional[ContactType] = None
    status: Optional[ContactStatus] = None
    priority: Optional[ContactPriority] = None
    assigned_to: Optional[UUID4] = None
    is_responded: Optional[bool] = None
    search: Optional[str] = None  # Search in name, email, subject, message