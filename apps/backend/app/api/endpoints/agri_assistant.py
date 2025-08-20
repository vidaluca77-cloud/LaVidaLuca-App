"""
Agricultural AI Assistant router.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import openai
import logging

from ...db.database import get_db
from ...models.models import Consultation, User
from ...schemas.schemas import ConsultationRequest, ConsultationResponse
from ...core.config import settings

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Configure OpenAI
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY
else:
    logger.warning("OpenAI API key not configured")

# Agricultural system prompt
AGRI_SYSTEM_PROMPT = """
Vous êtes un assistant agricole IA spécialisé dans l'agriculture durable et les pratiques agricoles en France.

Votre expertise couvre :
- Cultures céréalières et légumières
- Élevage (bovins, porcins, volailles, ovins)
- Viticulture et arboriculture
- Agriculture biologique et agroécologie
- Gestion des sols et fertilisation
- Protection phytosanitaire
- Techniques d'irrigation
- Météorologie agricole
- Réglementation agricole française et européenne
- Nouvelles technologies agricoles

Consignes :
1. Répondez toujours en français
2. Donnez des conseils pratiques et applicables
3. Mentionnez les réglementations françaises pertinentes si nécessaire
4. Adaptez vos conseils au contexte régional si mentionné
5. Encouragez les pratiques durables
6. Si vous n'êtes pas certain d'une information, recommandez de consulter un expert local
7. Gardez vos réponses concises mais complètes (300-500 mots max)
8. Structurez vos réponses avec des points clés

Répondez toujours de manière professionnelle et bienveillante.
"""


async def get_current_user(db: Session = Depends(get_db)) -> Optional[User]:
    """
    Get current user if authenticated (optional for consultations).
    For now, returns None (anonymous users allowed).
    TODO: Implement proper authentication when needed.
    """
    return None


@router.post("/consultation", response_model=ConsultationResponse, 
             summary="Create a new agricultural consultation")
async def create_consultation(
    request: ConsultationRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Create a new agricultural consultation with AI assistance.
    
    This endpoint accepts a question about agriculture and returns an AI-generated response
    specialized for agricultural practices in France.
    
    - **question**: The agricultural question to ask
    - **context**: Optional context (crop type, region, farming method, etc.)
    
    Returns the AI response along with metadata about the consultation.
    """
    try:
        # Validate OpenAI configuration
        if not settings.OPENAI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service d'IA agricole temporairement indisponible"
            )
        
        # Prepare the context information
        context_info = ""
        if request.context:
            context_items = []
            for key, value in request.context.items():
                if value:
                    context_items.append(f"{key}: {value}")
            if context_items:
                context_info = f"\n\nContexte: {', '.join(context_items)}"
        
        # Prepare the full prompt
        user_prompt = f"{request.question}{context_info}"
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": AGRI_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        # Save consultation to database
        consultation = Consultation(
            user_id=current_user.id if current_user else None,
            question=request.question,
            response=ai_response,
            context=request.context or {},
            model_used="gpt-3.5-turbo",
            tokens_used=tokens_used
        )
        
        db.add(consultation)
        db.commit()
        db.refresh(consultation)
        
        logger.info(f"Created consultation {consultation.id}, tokens used: {tokens_used}")
        
        return ConsultationResponse(
            id=consultation.id,
            user_id=consultation.user_id,
            question=consultation.question,
            response=consultation.response,
            context=consultation.context,
            model_used=consultation.model_used,
            tokens_used=consultation.tokens_used,
            created_at=consultation.created_at,
            updated_at=consultation.updated_at
        )
        
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Erreur du service d'IA. Veuillez réessayer plus tard."
        )
    except Exception as e:
        logger.error(f"Unexpected error in consultation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur inattendue s'est produite"
        )


@router.get("/consultations", response_model=List[ConsultationResponse],
            summary="Get consultation history")
async def get_consultations(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get consultation history.
    
    Returns recent consultations. If user is authenticated, returns their consultations.
    If not authenticated, returns recent public consultations (limited for privacy).
    """
    try:
        if current_user:
            # Return user's consultations
            consultations = db.query(Consultation).filter(
                Consultation.user_id == current_user.id
            ).order_by(Consultation.created_at.desc()).offset(skip).limit(limit).all()
        else:
            # Return recent anonymous consultations (limit sensitive info)
            consultations = db.query(Consultation).filter(
                Consultation.user_id.is_(None)
            ).order_by(Consultation.created_at.desc()).offset(skip).limit(min(limit, 5)).all()
        
        return [
            ConsultationResponse(
                id=c.id,
                user_id=c.user_id,
                question=c.question,
                response=c.response,
                context=c.context,
                model_used=c.model_used,
                tokens_used=c.tokens_used,
                created_at=c.created_at,
                updated_at=c.updated_at
            )
            for c in consultations
        ]
        
    except Exception as e:
        logger.error(f"Error fetching consultations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des consultations"
        )


@router.get("/consultation/{consultation_id}", response_model=ConsultationResponse,
            summary="Get a specific consultation")
async def get_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get a specific consultation by ID.
    """
    try:
        consultation = db.query(Consultation).filter(
            Consultation.id == consultation_id
        ).first()
        
        if not consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation non trouvée"
            )
        
        # Check access permissions
        if consultation.user_id and current_user:
            if consultation.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Accès non autorisé à cette consultation"
                )
        elif consultation.user_id and not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authentification requise pour accéder à cette consultation"
            )
        
        return ConsultationResponse(
            id=consultation.id,
            user_id=consultation.user_id,
            question=consultation.question,
            response=consultation.response,
            context=consultation.context,
            model_used=consultation.model_used,
            tokens_used=consultation.tokens_used,
            created_at=consultation.created_at,
            updated_at=consultation.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching consultation {consultation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération de la consultation"
        )