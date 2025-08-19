"""Booking API routes."""

from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...api.deps import get_current_active_user, get_current_instructor_or_admin
from ...db.session import get_db
from ...models.booking import Booking, BookingStatus
from ...models.user import User
from ...schemas.booking import (
    Booking as BookingSchema,
    BookingCreate,
    BookingUpdate,
    BookingWithDetails
)

router = APIRouter()


@router.get("/", response_model=List[BookingWithDetails])
def read_bookings(
    skip: int = 0,
    limit: int = 100,
    status: BookingStatus = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Retrieve bookings."""
    query = db.query(Booking)
    
    # Students can only see their own bookings
    if current_user.role == "student":
        query = query.filter(Booking.user_id == current_user.id)
    
    if status:
        query = query.filter(Booking.status == status)
    
    bookings = query.offset(skip).limit(limit).all()
    return bookings


@router.post("/", response_model=BookingSchema)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create new booking."""
    # Check if activity exists
    from ...models.activity import Activity
    activity = db.query(Activity).filter(Activity.id == booking_in.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user already has a booking for this activity
    existing_booking = (
        db.query(Booking)
        .filter(
            Booking.user_id == current_user.id,
            Booking.activity_id == booking_in.activity_id,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
        )
        .first()
    )
    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="You already have an active booking for this activity"
        )
    
    db_booking = Booking(
        user_id=current_user.id,
        **booking_in.dict()
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    return db_booking


@router.get("/{booking_id}", response_model=BookingWithDetails)
def read_booking(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get booking by ID."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Students can only see their own bookings
    if current_user.role == "student" and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return booking


@router.put("/{booking_id}", response_model=BookingSchema)
def update_booking(
    booking_id: UUID,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update booking."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Students can only update their own bookings
    if current_user.role == "student" and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Students cannot change status (except to cancel)
    if (current_user.role == "student" and 
        booking_update.status and 
        booking_update.status != BookingStatus.CANCELLED):
        raise HTTPException(
            status_code=403, 
            detail="Students can only cancel bookings"
        )
    
    booking_data = booking_update.dict(exclude_unset=True)
    for field, value in booking_data.items():
        setattr(booking, field, value)
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}")
def delete_booking(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Delete booking (instructor/admin only)."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}


@router.post("/{booking_id}/confirm")
def confirm_booking(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Confirm booking (instructor/admin only)."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = BookingStatus.CONFIRMED
    db.add(booking)
    db.commit()
    
    return {"message": "Booking confirmed successfully"}


@router.post("/{booking_id}/complete")
def complete_booking(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Complete booking (instructor/admin only)."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = BookingStatus.COMPLETED
    db.add(booking)
    db.commit()
    
    return {"message": "Booking completed successfully"}