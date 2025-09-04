from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import User
from app.schemas.schemas import (
    ActivityRegistration, ActivityRegistrationCreate, ActivityRegistrationUpdate,
    RegistrationWithDetails
)
from app.services.activity_service import ActivityRegistrationService
from app.auth.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[RegistrationWithDetails])
async def get_current_user_registrations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's activity registrations"""
    registration_service = ActivityRegistrationService(db)
    registrations = registration_service.get_user_registrations(current_user.id)
    
    # Apply pagination
    start = skip
    end = skip + limit
    paginated_registrations = registrations[start:end]
    
    # Load related data
    result = []
    for registration in paginated_registrations:
        result.append(RegistrationWithDetails(
            **ActivityRegistration.from_orm(registration).dict(),
            user=registration.user,
            activity=registration.activity,
            session=registration.session
        ))
    
    return result

@router.post("/", response_model=ActivityRegistration, status_code=status.HTTP_201_CREATED)
async def create_registration(
    registration_create: ActivityRegistrationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Register current user for an activity"""
    registration_service = ActivityRegistrationService(db)
    
    try:
        registration = registration_service.create_registration(
            current_user.id, 
            registration_create
        )
        return registration
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create registration"
        )

@router.get("/{registration_id}", response_model=RegistrationWithDetails)
async def get_registration(
    registration_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get registration by ID (only if it belongs to current user)"""
    registration_service = ActivityRegistrationService(db)
    
    registration = registration_service.get_registration(registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    # Check if registration belongs to current user
    if registration.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return RegistrationWithDetails(
        **ActivityRegistration.from_orm(registration).dict(),
        user=registration.user,
        activity=registration.activity,
        session=registration.session
    )

@router.put("/{registration_id}", response_model=ActivityRegistration)
async def update_registration(
    registration_id: int,
    registration_update: ActivityRegistrationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update registration (only if it belongs to current user)"""
    registration_service = ActivityRegistrationService(db)
    
    # First check if registration exists and belongs to user
    registration = registration_service.get_registration(registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    if registration.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    updated_registration = registration_service.update_registration(
        registration_id, 
        registration_update
    )
    
    if not updated_registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    return updated_registration

@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_registration(
    registration_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel registration (set status to cancelled)"""
    registration_service = ActivityRegistrationService(db)
    
    # First check if registration exists and belongs to user
    registration = registration_service.get_registration(registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    if registration.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update status to cancelled
    from app.schemas.schemas import ActivityRegistrationUpdate, RegistrationStatus
    cancelled_update = ActivityRegistrationUpdate(status=RegistrationStatus.CANCELLED)
    
    updated_registration = registration_service.update_registration(
        registration_id,
        cancelled_update
    )
    
    if not updated_registration:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel registration"
        )

# Admin endpoints (for demo purposes, available to all authenticated users)
@router.get("/activity/{activity_id}", response_model=List[RegistrationWithDetails])
async def get_activity_registrations(
    activity_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all registrations for an activity (admin endpoint)"""
    registration_service = ActivityRegistrationService(db)
    registrations = registration_service.get_activity_registrations(activity_id)
    
    # Apply pagination
    start = skip
    end = skip + limit
    paginated_registrations = registrations[start:end]
    
    # Load related data
    result = []
    for registration in paginated_registrations:
        result.append(RegistrationWithDetails(
            **ActivityRegistration.from_orm(registration).dict(),
            user=registration.user,
            activity=registration.activity,
            session=registration.session
        ))
    
    return result