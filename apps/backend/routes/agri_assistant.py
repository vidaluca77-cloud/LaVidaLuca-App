"""
Routes for agricultural AI assistant.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional, List
import uuid
import logging

from ..database import get_db_session
from ..models import AgriConsultation, User
from ..schemas.agri_assistant import (
    AgriConsultationRequest,
    AgriConsultationResponse,
    AgriConsultationHistory,
    AgriAssistantHealthResponse
)
from ..services.openai_service import get_agricultural_consultation
from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/agri-assistant", response_model=AgriConsultationResponse)
async def create_consultation(
    request: AgriConsultationRequest,
    db: AsyncSession = Depends(get_db_session),
    user_id: Optional[str] = None  # This would come from auth middleware in full implementation
):
    """
    Create a new agricultural consultation with AI assistance.
    """
    try:
        # Get AI response
        answer, category, confidence, tokens_used = await get_agricultural_consultation(
            question=request.question,
            context=request.context,
            user_profile={}  # Would be populated from authenticated user
        )
        
        # Create consultation record
        consultation = AgriConsultation(
            user_id=uuid.UUID(user_id) if user_id else None,
            question=request.question,
            answer=answer,
            ai_model=settings.OPENAI_MODEL,
            confidence_score=confidence,
            tokens_used=tokens_used,
            category=category or request.category,
            session_id=request.session_id
        )
        
        db.add(consultation)
        await db.commit()
        await db.refresh(consultation)
        
        return AgriConsultationResponse(
            id=consultation.id,
            question=consultation.question,
            answer=consultation.answer,
            ai_model=consultation.ai_model,
            confidence_score=consultation.confidence_score,
            tokens_used=consultation.tokens_used,
            category=consultation.category,
            session_id=consultation.session_id,
            created_at=consultation.created_at
        )
        
    except Exception as e:
        logger.error(f"Error creating consultation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors du traitement de votre consultation"
        )


@router.get("/agri-assistant/history", response_model=AgriConsultationHistory)
async def get_consultation_history(
    db: AsyncSession = Depends(get_db_session),
    user_id: Optional[str] = None,  # Would come from auth middleware
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    session_id: Optional[str] = Query(None, description="Filter by session ID")
):
    """
    Get consultation history for a user or all consultations if no user.
    """
    try:
        # Build query
        query = select(AgriConsultation)
        
        # Add filters
        if user_id:
            query = query.where(AgriConsultation.user_id == uuid.UUID(user_id))
        
        if category:
            query = query.where(AgriConsultation.category == category)
            
        if session_id:
            query = query.where(AgriConsultation.session_id == session_id)
        
        # Get total count
        count_query = query
        total_result = await db.execute(count_query)
        total_count = len(total_result.fetchall())
        
        # Add pagination and ordering
        query = query.order_by(desc(AgriConsultation.created_at))
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        # Execute query
        result = await db.execute(query)
        consultations = result.scalars().all()
        
        # Convert to response format
        consultation_responses = [
            AgriConsultationResponse(
                id=c.id,
                question=c.question,
                answer=c.answer,
                ai_model=c.ai_model,
                confidence_score=c.confidence_score,
                tokens_used=c.tokens_used,
                category=c.category,
                session_id=c.session_id,
                created_at=c.created_at
            )
            for c in consultations
        ]
        
        has_next = (page * page_size) < total_count
        
        return AgriConsultationHistory(
            consultations=consultation_responses,
            total_count=total_count,
            page=page,
            page_size=page_size,
            has_next=has_next
        )
        
    except Exception as e:
        logger.error(f"Error getting consultation history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors de la récupération de l'historique"
        )


@router.get("/agri-assistant/{consultation_id}", response_model=AgriConsultationResponse)
async def get_consultation(
    consultation_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific consultation by ID.
    """
    try:
        consultation_uuid = uuid.UUID(consultation_id)
        
        query = select(AgriConsultation).where(AgriConsultation.id == consultation_uuid)
        result = await db.execute(query)
        consultation = result.scalar_one_or_none()
        
        if not consultation:
            raise HTTPException(
                status_code=404,
                detail="Consultation non trouvée"
            )
        
        return AgriConsultationResponse(
            id=consultation.id,
            question=consultation.question,
            answer=consultation.answer,
            ai_model=consultation.ai_model,
            confidence_score=consultation.confidence_score,
            tokens_used=consultation.tokens_used,
            category=consultation.category,
            session_id=consultation.session_id,
            created_at=consultation.created_at
        )
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="ID de consultation invalide"
        )
    except Exception as e:
        logger.error(f"Error getting consultation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors de la récupération de la consultation"
        )


@router.get("/agri-assistant-health", response_model=AgriAssistantHealthResponse)
async def agri_assistant_health(db: AsyncSession = Depends(get_db_session)):
    """
    Health check for agricultural assistant service.
    """
    try:
        # Get last consultation time
        query = select(AgriConsultation.created_at).order_by(desc(AgriConsultation.created_at)).limit(1)
        result = await db.execute(query)
        last_consultation = result.scalar_one_or_none()
        
        return AgriAssistantHealthResponse(
            status="healthy",
            ai_enabled=settings.OPENAI_API_KEY is not None,
            model=settings.OPENAI_MODEL,
            last_consultation=last_consultation
        )
        
    except Exception as e:
        logger.error(f"Error in agri-assistant health check: {str(e)}")
        return AgriAssistantHealthResponse(
            status="degraded",
            ai_enabled=False,
            model=settings.OPENAI_MODEL,
            last_consultation=None
        )