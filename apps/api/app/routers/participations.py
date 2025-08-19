from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User, Activity, Participation
from app.schemas.participation import (
    Participation as ParticipationSchema, 
    ParticipationCreate, 
    ParticipationUpdate,
    ParticipationWithActivity,
    ParticipationWithUser
)
from app.utils.auth import get_current_active_user, get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[ParticipationWithActivity])
def read_participations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's participations."""
    participations = db.query(Participation).filter(
        Participation.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    # Add activity details
    participations_with_activity = []
    for participation in participations:
        activity = db.query(Activity).filter(Activity.id == participation.activity_id).first()
        participation_data = ParticipationWithActivity(
            **participation.__dict__,
            activity=activity.__dict__ if activity else None
        )
        participations_with_activity.append(participation_data)
    
    return participations_with_activity


@router.get("/admin", response_model=List[ParticipationWithUser])
def read_all_participations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all participations (admin only)."""
    participations = db.query(Participation).offset(skip).limit(limit).all()
    
    # Add user details
    participations_with_user = []
    for participation in participations:
        user = db.query(User).filter(User.id == participation.user_id).first()
        activity = db.query(Activity).filter(Activity.id == participation.activity_id).first()
        
        participation_data = ParticipationWithUser(
            **participation.__dict__,
            user=user.__dict__ if user else None,
            activity=activity.__dict__ if activity else None
        )
        participations_with_user.append(participation_data)
    
    return participations_with_user


@router.get("/{participation_id}", response_model=ParticipationWithActivity)
def read_participation(
    participation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get participation by ID."""
    participation = db.query(Participation).filter(Participation.id == participation_id).first()
    if participation is None:
        raise HTTPException(status_code=404, detail="Participation not found")
    
    # Users can only see their own participations or admins can see any
    if participation.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    activity = db.query(Activity).filter(Activity.id == participation.activity_id).first()
    
    return ParticipationWithActivity(
        **participation.__dict__,
        activity=activity.__dict__ if activity else None
    )


@router.post("/", response_model=ParticipationSchema)
def create_participation(
    participation: ParticipationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Register for an activity."""
    # Check if activity exists
    activity = db.query(Activity).filter(Activity.id == participation.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    if not activity.is_active:
        raise HTTPException(status_code=400, detail="Activity is not active")
    
    # Check if user is already registered
    existing = db.query(Participation).filter(
        Participation.user_id == current_user.id,
        Participation.activity_id == participation.activity_id,
        Participation.status.in_(["registered", "confirmed"])
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already registered for this activity")
    
    # Check if activity is full
    current_participants = db.query(Participation).filter(
        Participation.activity_id == participation.activity_id,
        Participation.status.in_(["registered", "confirmed"])
    ).count()
    
    if current_participants >= activity.max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")
    
    # Create participation
    db_participation = Participation(
        user_id=current_user.id,
        activity_id=participation.activity_id,
        scheduled_date=participation.scheduled_date,
        status=participation.status or "registered"
    )
    
    db.add(db_participation)
    db.commit()
    db.refresh(db_participation)
    
    return db_participation


@router.put("/{participation_id}", response_model=ParticipationSchema)
def update_participation(
    participation_id: int,
    participation_update: ParticipationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update participation."""
    participation = db.query(Participation).filter(Participation.id == participation_id).first()
    if participation is None:
        raise HTTPException(status_code=404, detail="Participation not found")
    
    # Users can only update their own participations or admins can update any
    if participation.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = participation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(participation, field, value)
    
    db.commit()
    db.refresh(participation)
    
    return participation


@router.delete("/{participation_id}")
def cancel_participation(
    participation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel participation."""
    participation = db.query(Participation).filter(Participation.id == participation_id).first()
    if participation is None:
        raise HTTPException(status_code=404, detail="Participation not found")
    
    # Users can only cancel their own participations or admins can cancel any
    if participation.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update status to cancelled instead of deleting
    participation.status = "cancelled"
    db.commit()
    
    return {"message": "Participation cancelled successfully"}