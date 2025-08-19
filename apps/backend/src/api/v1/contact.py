"""
Contact form API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from ...core.dependencies import standard_rate_limit
from ...schemas.activity import ContactForm
from ...services.email import EmailService
from ...services.openai import OpenAIService

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("/", response_model=dict)
@standard_rate_limit
async def submit_contact_form(
    form_data: ContactForm
):
    """Submit contact form."""
    
    # Moderate content using OpenAI
    openai_service = OpenAIService()
    
    # Check message content
    message_moderation = await openai_service.moderate_content(form_data.message)
    if message_moderation.get("flagged", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content is inappropriate"
        )
    
    # Check subject content
    subject_moderation = await openai_service.moderate_content(form_data.subject)
    if subject_moderation.get("flagged", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject content is inappropriate"
        )
    
    # Send email
    email_service = EmailService()
    email_sent = await email_service.send_contact_form_submission(form_data)
    
    if not email_sent:
        # Don't fail the request if email fails - log it instead
        # In production, you'd want proper logging here
        pass
    
    return {
        "message": "Contact form submitted successfully",
        "email_sent": email_sent
    }


@router.get("/info", response_model=dict)
async def get_contact_info():
    """Get contact information."""
    
    return {
        "email": "contact@lavidaluca.fr",
        "phone": "+33 1 23 45 67 89",
        "address": "123 Rue de la Agriculture, 12345 Ville, France",
        "hours": "Lundi - Vendredi: 9h00 - 17h00",
        "social_media": {
            "facebook": "https://facebook.com/lavidaluca",
            "instagram": "https://instagram.com/lavidaluca",
            "twitter": "https://twitter.com/lavidaluca"
        }
    }