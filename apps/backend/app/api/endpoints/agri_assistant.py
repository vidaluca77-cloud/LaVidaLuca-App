import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from openai import OpenAI

from ...db.database import get_db
from ...core.config import settings
from ...models.models import Consultation, User
from ...schemas.schemas import ConsultationCreate, ConsultationResponse, Consultation as ConsultationSchema
from ..deps import get_current_user_optional

router = APIRouter()


@router.post("/ask", response_model=ConsultationResponse)
async def ask_agricultural_assistant(
    consultation_data: ConsultationCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Ask the agricultural AI assistant a question.
    Supports both authenticated and anonymous users.
    """
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured"
        )
    
    try:
        # Configure OpenAI client
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Create specialized agricultural prompt
        system_prompt = """Tu es un assistant agricole expert spécialisé dans l'agriculture française et européenne. 
        Tu aides les agriculteurs, éleveurs et jardiniers avec leurs questions sur:
        - Les techniques de culture et d'élevage
        - La gestion des sols et la fertilisation
        - La lutte contre les maladies et ravageurs
        - Les pratiques d'agriculture durable et biologique
        - Les réglementations agricoles
        - Les cycles de plantation et récolte
        - L'optimisation des rendements
        - La gestion de l'eau et l'irrigation
        
        Réponds toujours en français, de manière claire et pratique. 
        Si la question n'est pas liée à l'agriculture, réponds poliment que tu ne peux aider que sur les sujets agricoles.
        Fournis des réponses précises, pratiques et basées sur les bonnes pratiques agricoles.
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": consultation_data.question}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Save consultation to database
        consultation = Consultation(
            question=consultation_data.question,
            response=ai_response,
            category=consultation_data.category,
            user_id=current_user.id if current_user else None,
            session_id=consultation_data.session_id if not current_user else None
        )
        
        db.add(consultation)
        db.commit()
        db.refresh(consultation)
        
        return ConsultationResponse(response=ai_response)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing agricultural consultation: {str(e)}"
        )


@router.get("/history", response_model=List[ConsultationSchema])
async def get_consultation_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get consultation history for authenticated users or by session ID for anonymous users.
    """
    query = db.query(Consultation)
    
    if current_user:
        # For authenticated users, get their consultations
        query = query.filter(Consultation.user_id == current_user.id)
    elif session_id:
        # For anonymous users, get consultations by session ID
        query = query.filter(Consultation.session_id == session_id)
    else:
        raise HTTPException(
            status_code=400,
            detail="Either authentication or session_id is required"
        )
    
    consultations = query.order_by(desc(Consultation.created_at)).offset(skip).limit(limit).all()
    return consultations


@router.get("/categories")
async def get_consultation_categories():
    """
    Get available consultation categories.
    """
    return {
        "categories": [
            {"value": "agriculture", "label": "Agriculture générale"},
            {"value": "elevage", "label": "Élevage"},
            {"value": "jardinage", "label": "Jardinage"},
            {"value": "sols", "label": "Gestion des sols"},
            {"value": "maladies", "label": "Maladies et ravageurs"},
            {"value": "irrigation", "label": "Irrigation et eau"},
            {"value": "bio", "label": "Agriculture biologique"},
            {"value": "reglementation", "label": "Réglementation"},
        ]
    }


@router.delete("/{consultation_id}")
async def delete_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """
    Delete a consultation (only for the owner).
    """
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id
    ).first()
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    # Check ownership
    if current_user and consultation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this consultation")
    elif not current_user and not consultation.session_id:
        raise HTTPException(status_code=403, detail="Cannot delete consultation without proper authorization")
    
    db.delete(consultation)
    db.commit()
    
    return {"message": "Consultation deleted successfully"}