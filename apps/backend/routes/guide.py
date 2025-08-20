"""
Guide endpoint for AI-powered agricultural assistance.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from ..database import get_db_session
from ..models.user import User
from ..models.consultation import Consultation
from ..auth.dependencies import get_current_active_user
from ..services.openai_service import get_agricultural_consultation

logger = logging.getLogger(__name__)

router = APIRouter()


class GuideRequest(BaseModel):
    """Request model for guide endpoint."""
    question: str
    context: Optional[str] = None


class GuideResponse(BaseModel):
    """Response model for guide endpoint."""
    answer: str
    confidence: Optional[str] = None
    sources: Optional[List[str]] = None
    consultation_id: Optional[str] = None


class ConsultationHistoryResponse(BaseModel):
    """Response model for consultation history."""
    consultations: List[dict]
    total: int


class ConsultationFeedbackRequest(BaseModel):
    """Request model for consultation feedback."""
    is_helpful: Optional[bool] = None
    user_rating: Optional[str] = None  # "1" to "5"


@router.post("/guide", response_model=GuideResponse)
async def get_agricultural_guide(
    request: GuideRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get AI-powered agricultural guidance with conversation history storage.
    
    This endpoint provides helpful advice and guidance for questions related to:
    - Sustainable agriculture and farming practices
    - Gardening and permaculture
    - Plant diseases and pest management
    - Soil health and composting
    - Irrigation and water management
    - Crop rotation and companion planting
    """
    try:
        # Get AI response
        ai_answer, metadata = await get_agricultural_consultation(
            question=request.question,
            context=request.context,
            user_location=current_user.profile.get('location') if current_user.profile else None
        )
        
        # Determine category based on question keywords
        category = _categorize_question(request.question)
        
        # Extract tags from question
        tags = _extract_tags(request.question)
        
        # Save consultation to database
        consultation = Consultation(
            user_id=current_user.id,
            question=request.question,
            answer=ai_answer,
            context=request.context,
            ai_model=metadata.get("model", "gpt-4"),
            confidence_score=metadata.get("confidence", "medium"),
            tokens_used=metadata.get("tokens_used", "unknown"),
            category=category,
            tags=tags
        )
        
        db.add(consultation)
        await db.commit()
        await db.refresh(consultation)
        
        return GuideResponse(
            answer=ai_answer,
            confidence=metadata.get("confidence", "medium"),
            sources=["Assistant IA Agricole La Vida Luca", "Base de connaissances en agriculture durable"],
            consultation_id=str(consultation.id)
        )
        
    except Exception as e:
        logger.error(f"Error in agricultural guide endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors du traitement de votre question agricole"
        )


@router.get("/guide/history", response_model=ConsultationHistoryResponse)
async def get_consultation_history(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
    limit: int = 20,
    offset: int = 0
):
    """
    Get user's consultation history.
    """
    try:
        # Get user's consultations with pagination
        result = await db.execute(
            select(Consultation)
            .where(Consultation.user_id == current_user.id)
            .order_by(Consultation.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        consultations = result.scalars().all()
        
        # Get total count
        count_result = await db.execute(
            select(Consultation)
            .where(Consultation.user_id == current_user.id)
        )
        total = len(count_result.scalars().all())
        
        return ConsultationHistoryResponse(
            consultations=[consultation.to_dict_summary() for consultation in consultations],
            total=total
        )
        
    except Exception as e:
        logger.error(f"Error fetching consultation history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération de l'historique"
        )


@router.get("/guide/consultation/{consultation_id}")
async def get_consultation_detail(
    consultation_id: str,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed consultation information.
    """
    try:
        result = await db.execute(
            select(Consultation)
            .where(
                Consultation.id == consultation_id,
                Consultation.user_id == current_user.id
            )
        )
        
        consultation = result.scalar_one_or_none()
        
        if not consultation:
            raise HTTPException(
                status_code=404,
                detail="Consultation non trouvée"
            )
        
        return consultation.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching consultation detail: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération de la consultation"
        )


@router.post("/guide/consultation/{consultation_id}/feedback")
async def submit_consultation_feedback(
    consultation_id: str,
    feedback: ConsultationFeedbackRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Submit feedback for a consultation.
    """
    try:
        result = await db.execute(
            select(Consultation)
            .where(
                Consultation.id == consultation_id,
                Consultation.user_id == current_user.id
            )
        )
        
        consultation = result.scalar_one_or_none()
        
        if not consultation:
            raise HTTPException(
                status_code=404,
                detail="Consultation non trouvée"
            )
        
        # Update feedback
        if feedback.is_helpful is not None:
            consultation.is_helpful = feedback.is_helpful
        if feedback.user_rating is not None:
            consultation.user_rating = feedback.user_rating
        
        await db.commit()
        
        return {"message": "Feedback enregistré avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de l'enregistrement du feedback"
        )


@router.get("/guide/health")
async def guide_health():
    """Health check for guide service."""
    from ..config import settings
    return {
        "status": "healthy",
        "service": "agricultural_guide",
        "ai_enabled": hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY is not None
    }


def _categorize_question(question: str) -> str:
    """Categorize the question based on keywords."""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["sol", "terre", "ph", "compost", "fertilisation"]):
        return "sol_nutrition"
    elif any(word in question_lower for word in ["maladie", "ravageur", "parasite", "puceron", "traitement"]):
        return "maladies_ravageurs"
    elif any(word in question_lower for word in ["arrosage", "irrigation", "eau", "sécheresse"]):
        return "irrigation"
    elif any(word in question_lower for word in ["semis", "plantation", "graine", "bouture"]):
        return "plantation"
    elif any(word in question_lower for word in ["récolte", "conservation", "stockage"]):
        return "recolte"
    elif any(word in question_lower for word in ["permaculture", "durable", "écologique", "bio"]):
        return "permaculture"
    else:
        return "agriculture"


def _extract_tags(question: str) -> List[str]:
    """Extract relevant tags from the question."""
    question_lower = question.lower()
    tags = []
    
    # Common agricultural terms
    tag_keywords = {
        "tomate": "tomates",
        "potager": "potager",
        "jardin": "jardinage",
        "bio": "agriculture_bio",
        "compost": "compostage",
        "paillis": "paillage",
        "permaculture": "permaculture",
        "serre": "culture_sous_serre",
        "légume": "légumes",
        "fruit": "fruits",
        "herbe": "désherbage",
        "insecte": "gestion_ravageurs"
    }
    
    for keyword, tag in tag_keywords.items():
        if keyword in question_lower:
            tags.append(tag)
    
    return tags[:5]  # Limit to 5 tags