from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime
from ..db.database import get_db
from ..models.models import ActivityRegistration, Activity, ActivitySession, User, RegistrationStatus
from ..schemas.schemas import (
    ActivityRegistration as ActivityRegistrationSchema,
    ActivityRegistrationCreate,
    ActivityRegistrationUpdate,
    ActivitySession as ActivitySessionSchema,
    ActivitySessionCreate,
    ActivitySessionUpdate
)
from ..auth.dependencies import get_current_active_user, get_current_instructor_or_admin
from ..core.logging import log_info, log_error

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.get("/", response_model=List[ActivityRegistrationSchema])
def get_user_registrations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: Optional[RegistrationStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's activity registrations."""
    query = db.query(ActivityRegistration).filter(ActivityRegistration.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(ActivityRegistration.status == status_filter)
    
    registrations = query.offset(skip).limit(limit).all()
    return registrations


@router.get("/{registration_id}", response_model=ActivityRegistrationSchema)
def get_registration(
    registration_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific registration by ID."""
    registration = db.query(ActivityRegistration).filter(
        ActivityRegistration.id == registration_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    # Check if user can access this registration
    if (registration.user_id != current_user.id and 
        current_user.role not in ["instructor", "admin"]):
        # For instructors, check if they own the activity
        if current_user.role == "instructor":
            activity = db.query(Activity).filter(Activity.id == registration.activity_id).first()
            if not activity or activity.instructor_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    return registration


@router.post("/", response_model=ActivityRegistrationSchema, status_code=status.HTTP_201_CREATED)
def create_registration(
    registration_data: ActivityRegistrationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Register for an activity session."""
    # Check if activity exists and is active
    activity = db.query(Activity).filter(
        and_(
            Activity.id == registration_data.activity_id,
            Activity.is_active == True
        )
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found or inactive"
        )
    
    # Check if session exists and is not cancelled
    session = db.query(ActivitySession).filter(
        and_(
            ActivitySession.id == registration_data.session_id,
            ActivitySession.activity_id == registration_data.activity_id,
            ActivitySession.is_cancelled == False
        )
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or cancelled"
        )
    
    # Check if session is in the future
    if session.start_date <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot register for past sessions"
        )
    
    # Check if user is already registered for this session
    existing_registration = db.query(ActivityRegistration).filter(
        and_(
            ActivityRegistration.user_id == current_user.id,
            ActivityRegistration.session_id == registration_data.session_id,
            ActivityRegistration.status != RegistrationStatus.CANCELLED
        )
    ).first()
    
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered for this session"
        )
    
    # Check if session has available spots
    current_registrations = db.query(ActivityRegistration).filter(
        and_(
            ActivityRegistration.session_id == registration_data.session_id,
            ActivityRegistration.status.in_([RegistrationStatus.PENDING, RegistrationStatus.CONFIRMED])
        )
    ).count()
    
    if current_registrations >= session.available_spots:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No available spots for this session"
        )
    
    # Create registration
    new_registration = ActivityRegistration(
        user_id=current_user.id,
        activity_id=registration_data.activity_id,
        session_id=registration_data.session_id,
        registration_notes=registration_data.registration_notes,
        status=RegistrationStatus.PENDING
    )
    
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    
    log_info(f"User registered for activity: {current_user.email} -> {activity.title}")
    return new_registration


@router.put("/{registration_id}", response_model=ActivityRegistrationSchema)
def update_registration(
    registration_id: int,
    registration_update: ActivityRegistrationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a registration."""
    registration = db.query(ActivityRegistration).filter(
        ActivityRegistration.id == registration_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    # Check permissions
    can_update = False
    
    if registration.user_id == current_user.id:
        # User can only update their own registration notes
        can_update = True
        allowed_fields = ["registration_notes"]
    elif current_user.role == "admin":
        # Admin can update everything
        can_update = True
        allowed_fields = None
    elif current_user.role == "instructor":
        # Instructor can update if they own the activity
        activity = db.query(Activity).filter(Activity.id == registration.activity_id).first()
        if activity and activity.instructor_id == current_user.id:
            can_update = True
            allowed_fields = ["status", "completion_notes", "rating", "feedback"]
    
    if not can_update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update only allowed fields
    update_data = registration_update.dict(exclude_unset=True)
    
    if allowed_fields:
        update_data = {k: v for k, v in update_data.items() if k in allowed_fields}
    
    # Handle completion logic
    if "status" in update_data and update_data["status"] == RegistrationStatus.COMPLETED:
        update_data["completion_date"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(registration, field, value)
    
    db.commit()
    db.refresh(registration)
    
    log_info(f"Registration updated: {registration_id} by {current_user.email}")
    return registration


@router.delete("/{registration_id}")
def cancel_registration(
    registration_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel a registration."""
    registration = db.query(ActivityRegistration).filter(
        ActivityRegistration.id == registration_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    # Check if user can cancel this registration
    if (registration.user_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Cannot cancel completed registrations
    if registration.status == RegistrationStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel completed registration"
        )
    
    # Update status to cancelled
    registration.status = RegistrationStatus.CANCELLED
    db.commit()
    
    log_info(f"Registration cancelled: {registration_id} by {current_user.email}")
    return {"message": "Registration cancelled successfully"}


# Activity sessions management (for instructors)
sessions_router = APIRouter(prefix="/sessions", tags=["activity-sessions"])


@sessions_router.get("/activity/{activity_id}", response_model=List[ActivitySessionSchema])
def get_activity_sessions(
    activity_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    include_cancelled: bool = False,
    db: Session = Depends(get_db)
):
    """Get sessions for a specific activity."""
    # Check if activity exists
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    query = db.query(ActivitySession).filter(ActivitySession.activity_id == activity_id)
    
    if not include_cancelled:
        query = query.filter(ActivitySession.is_cancelled == False)
    
    sessions = query.offset(skip).limit(limit).all()
    return sessions


@sessions_router.post("/", response_model=ActivitySessionSchema, status_code=status.HTTP_201_CREATED)
def create_activity_session(
    session_data: ActivitySessionCreate,
    current_user: User = Depends(get_current_instructor_or_admin),
    db: Session = Depends(get_db)
):
    """Create a new activity session."""
    # Check if activity exists and user can create sessions for it
    activity = db.query(Activity).filter(Activity.id == session_data.activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions
    if current_user.role != "admin" and activity.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create sessions for this activity"
        )
    
    # Validate session timing
    if session_data.end_date <= session_data.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    # Create session
    new_session = ActivitySession(**session_data.dict())
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    log_info(f"Activity session created for {activity.title} by {current_user.email}")
    return new_session


# Include sessions router
router.include_router(sessions_router)