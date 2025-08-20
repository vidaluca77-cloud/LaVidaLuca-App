"""
Consultation routes for agricultural AI assistant.
"""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.orm import selectinload

from ..database import get_db_session
from ..models import Consultation, User
from ..schemas.consultation import (
    ConsultationCreate, ConsultationResponse, ConsultationList,
    ConsultationQuery, AIAssistantRequest, AIAssistantResponse
)
from ..auth.dependencies import get_current_user
from ..services.openai_service import get_agricultural_consultation
from ..monitoring import api_logger
from ..config import settings

router = APIRouter()
security = HTTPBearer()


@router.post("/consultations/ask", response_model=AIAssistantResponse)
async def ask_agricultural_assistant(
    request: AIAssistantRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Ask the agricultural AI assistant a question.
    Creates a new consultation and returns the AI response.
    """
    api_logger.info(
        "Agricultural consultation request",
        user_id=str(current_user.id),
        question_length=len(request.question)
    )
    
    try:
        # Get AI response
        answer, category, tags, response_time = await get_agricultural_consultation(
            question=request.question,
            context=request.context
        )
        
        # Create consultation record
        consultation = Consultation(
            user_id=current_user.id,
            question=request.question,
            answer=answer,
            category=category,
            tags=tags,
            ai_model=getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo'),
            response_time=response_time,
            session_id=str(uuid.uuid4())  # New session for each question
        )
        
        db.add(consultation)
        await db.commit()
        await db.refresh(consultation)
        
        api_logger.info(
            "Agricultural consultation completed",
            consultation_id=str(consultation.id),
            category=category,
            response_time=response_time
        )
        
        return AIAssistantResponse(
            answer=answer,
            category=category,
            tags=tags,
            response_time=response_time,
            consultation_id=str(consultation.id)
        )
        
    except Exception as e:
        api_logger.error("Agricultural consultation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process agricultural consultation"
        )


@router.get("/consultations", response_model=ConsultationList)
async def list_consultations(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    session_id: Optional[str] = Query(None, description="Filter by session"),
    search: Optional[str] = Query(None, min_length=3, description="Search in questions and answers"),
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    List user's consultations with pagination and filtering.
    """
    # Build query
    query = select(Consultation).where(Consultation.user_id == current_user.id)
    
    # Apply filters
    if category:
        query = query.where(Consultation.category == category)
    
    if session_id:
        query = query.where(Consultation.session_id == session_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Consultation.question.ilike(search_term),
                Consultation.answer.ilike(search_term)
            )
        )
    
    # Get total count
    count_query = select(func.count()).select_from(
        query.subquery()
    )
    total = await db.scalar(count_query)
    
    # Apply pagination and ordering
    query = query.order_by(desc(Consultation.created_at))
    query = query.offset((page - 1) * per_page).limit(per_page)
    
    # Execute query
    result = await db.execute(query)
    consultations = result.scalars().all()
    
    # Convert to response format
    consultation_responses = [
        ConsultationResponse.from_orm(consultation)
        for consultation in consultations
    ]
    
    return ConsultationList(
        consultations=consultation_responses,
        total=total,
        page=page,
        per_page=per_page,
        has_next=(page * per_page) < total,
        has_prev=page > 1
    )


@router.get("/consultations/{consultation_id}", response_model=ConsultationResponse)
async def get_consultation(
    consultation_id: str,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific consultation by ID.
    """
    try:
        consultation_uuid = uuid.UUID(consultation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid consultation ID format"
        )
    
    query = select(Consultation).where(
        and_(
            Consultation.id == consultation_uuid,
            Consultation.user_id == current_user.id
        )
    )
    
    result = await db.execute(query)
    consultation = result.scalar_one_or_none()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    return ConsultationResponse.from_orm(consultation)


@router.delete("/consultations/{consultation_id}")
async def delete_consultation(
    consultation_id: str,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a consultation.
    """
    try:
        consultation_uuid = uuid.UUID(consultation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid consultation ID format"
        )
    
    query = select(Consultation).where(
        and_(
            Consultation.id == consultation_uuid,
            Consultation.user_id == current_user.id
        )
    )
    
    result = await db.execute(query)
    consultation = result.scalar_one_or_none()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    await db.delete(consultation)
    await db.commit()
    
    return {"message": "Consultation deleted successfully"}


@router.get("/consultations/categories/stats")
async def get_consultation_stats(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get consultation statistics by category for the current user.
    """
    query = select(
        Consultation.category,
        func.count(Consultation.id).label('count')
    ).where(
        Consultation.user_id == current_user.id
    ).group_by(Consultation.category)
    
    result = await db.execute(query)
    stats = result.all()
    
    return {
        "categories": [
            {"category": row.category, "count": row.count}
            for row in stats
        ],
        "total_consultations": sum(row.count for row in stats)
    }