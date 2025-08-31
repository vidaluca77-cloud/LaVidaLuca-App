"""
Contact form endpoints for the FastAPI app structure.
This is a simplified version based on the main contacts.py in routes directory.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


router = APIRouter()


class ContactType(str, Enum):
    """Contact request types."""

    GENERAL = "general"
    PARTNERSHIP = "partnership"
    SUPPORT = "support"
    FEEDBACK = "feedback"
    COLLABORATION = "collaboration"
    PRESS = "press"


class ContactCreate(BaseModel):
    """Contact creation schema."""

    name: str = Field(..., max_length=255)
    email: EmailStr
    phone: str = Field(None, max_length=50)
    organization: str = Field(None, max_length=255)
    subject: str = Field(..., max_length=500)
    message: str = Field(..., min_length=10)
    contact_type: ContactType = ContactType.GENERAL
    consent_privacy: bool = True
    consent_marketing: bool = False

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
                "consent_marketing": False,
            }
        }


class ContactResponse(BaseModel):
    """Contact response schema."""

    id: str
    name: str
    email: EmailStr
    subject: str
    message: str
    contact_type: str
    status: str = "new"
    created_at: str

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Jean Dupont",
                "email": "jean.dupont@example.com",
                "subject": "Demande de partenariat",
                "message": "Bonjour, nous souhaitons explorer une collaboration...",
                "contact_type": "partnership",
                "status": "new",
                "created_at": "2024-01-15T10:30:00Z",
            }
        }


@router.post("/", response_model=ContactResponse, summary="Submit contact form")
def create_contact(contact_data: ContactCreate):
    """
    Submit a new contact form (public endpoint).

    This endpoint allows users to submit contact forms without authentication.
    All submissions are stored for review by administrators.

    - **name**: Full name of the person submitting the form
    - **email**: Valid email address for contact
    - **subject**: Brief subject line for the inquiry
    - **message**: Detailed message (minimum 10 characters)
    - **contact_type**: Type of inquiry (general, partnership, support, etc.)
    - **consent_privacy**: Required consent for privacy policy
    - **consent_marketing**: Optional consent for marketing communications
    """
    # In a real implementation, this would save to database
    # For now, return a mock response
    import uuid
    from datetime import datetime

    return ContactResponse(
        id=str(uuid.uuid4()),
        name=contact_data.name,
        email=contact_data.email,
        subject=contact_data.subject,
        message=contact_data.message,
        contact_type=contact_data.contact_type.value,
        status="new",
        created_at=datetime.utcnow().isoformat() + "Z",
    )


@router.get("/types", response_model=List[str], summary="Get contact types")
def get_contact_types():
    """
    Get available contact form types.

    Returns a list of all available contact types that can be used
    when submitting a contact form.
    """
    return [contact_type.value for contact_type in ContactType]
