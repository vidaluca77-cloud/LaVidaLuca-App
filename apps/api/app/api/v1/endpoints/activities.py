from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import User
from app.schemas.schemas import (
    Activity, ActivityCreate, ActivityUpdate, ActivityWithSessions,
    ActivitySession, ActivitySessionCreate, ActivitySessionUpdate,
    ActivityCategory
)
from app.services.activity_service import ActivityService, ActivitySessionService
from app.auth.dependencies import get_current_active_user, require_mfr_student

router = APIRouter()

@router.get("/", response_model=List[Activity])
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[ActivityCategory] = Query(None),
    requires_mfr: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of activities (public endpoint)"""
    activity_service = ActivityService(db)
    activities = activity_service.get_activities(
        skip=skip,
        limit=limit,
        category=category,
        requires_mfr=requires_mfr,
        is_active=True
    )
    return activities

@router.get("/recommendations", response_model=List[dict])
async def get_activity_recommendations(
    limit: int = Query(10, ge=1, le=20),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized activity recommendations for current user"""
    activity_service = ActivityService(db)
    recommendations = activity_service.get_recommended_activities(current_user, limit=limit)
    return recommendations

@router.get("/{activity_id}", response_model=ActivityWithSessions)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    """Get activity by ID with sessions"""
    activity_service = ActivityService(db)
    session_service = ActivitySessionService(db)
    
    activity = activity_service.get_activity(activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    sessions = session_service.get_sessions_for_activity(activity_id)
    
    return ActivityWithSessions(
        **Activity.from_orm(activity).dict(),
        sessions=sessions
    )

@router.get("/slug/{slug}", response_model=ActivityWithSessions)
async def get_activity_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get activity by slug with sessions"""
    activity_service = ActivityService(db)
    session_service = ActivitySessionService(db)
    
    activity = activity_service.get_activity_by_slug(slug)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    sessions = session_service.get_sessions_for_activity(activity.id)
    
    return ActivityWithSessions(
        **Activity.from_orm(activity).dict(),
        sessions=sessions
    )

@router.post("/", response_model=Activity, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_create: ActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create new activity (admin only - for demo purposes, any authenticated user can create)"""
    activity_service = ActivityService(db)
    
    try:
        activity = activity_service.create_activity(activity_create)
        return activity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create activity"
        )

@router.put("/{activity_id}", response_model=Activity)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update activity (admin only - for demo purposes, any authenticated user can update)"""
    activity_service = ActivityService(db)
    
    updated_activity = activity_service.update_activity(activity_id, activity_update)
    if not updated_activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return updated_activity

@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete activity (soft delete - admin only)"""
    activity_service = ActivityService(db)
    
    success = activity_service.delete_activity(activity_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

# Session endpoints
@router.get("/{activity_id}/sessions", response_model=List[ActivitySession])
async def get_activity_sessions(
    activity_id: int,
    db: Session = Depends(get_db)
):
    """Get all sessions for an activity"""
    activity_service = ActivityService(db)
    session_service = ActivitySessionService(db)
    
    # Verify activity exists
    activity = activity_service.get_activity(activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    sessions = session_service.get_sessions_for_activity(activity_id)
    return sessions

@router.post("/{activity_id}/sessions", response_model=ActivitySession, status_code=status.HTTP_201_CREATED)
async def create_activity_session(
    activity_id: int,
    session_create: ActivitySessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create new session for an activity"""
    # Ensure the activity_id in the URL matches the one in the request body
    session_create.activity_id = activity_id
    
    session_service = ActivitySessionService(db)
    
    try:
        session = session_service.create_session(session_create)
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create session"
        )

@router.put("/sessions/{session_id}", response_model=ActivitySession)
async def update_activity_session(
    session_id: int,
    session_update: ActivitySessionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update activity session"""
    session_service = ActivitySessionService(db)
    
    updated_session = session_service.update_session(session_id, session_update)
    if not updated_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return updated_session

@router.get("/sessions/{session_id}", response_model=ActivitySession)
async def get_activity_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Get activity session by ID"""
    session_service = ActivitySessionService(db)
    
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session