"""
Bookings API endpoints
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_active_user
from app.models.models import Booking as BookingModel, Activity, User
from app.schemas.schemas import (
    Booking,
    BookingCreate,
    BookingUpdate,
    BookingStatus,
    PaginatedResponse,
    APIResponse
)

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
async def get_user_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status_filter: Optional[BookingStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's bookings"""
    
    query = db.query(BookingModel).filter(BookingModel.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(BookingModel.status == status_filter)
    
    total = query.count()
    bookings = query.offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=bookings,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@router.get("/{booking_id}", response_model=Booking)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific booking"""
    
    booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    return booking

@router.post("/", response_model=APIResponse)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new booking"""
    
    # Verify activity exists
    activity = db.query(Activity).filter(
        Activity.id == booking_data.activity_id,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if booking date is in the future
    if booking_data.scheduled_date <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking date must be in the future"
        )
    
    # Check for existing booking at the same time
    existing_booking = db.query(BookingModel).filter(
        BookingModel.user_id == current_user.id,
        BookingModel.scheduled_date == booking_data.scheduled_date,
        BookingModel.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a booking at this time"
        )
    
    # Create booking
    db_booking = BookingModel(
        user_id=current_user.id,
        activity_id=booking_data.activity_id,
        scheduled_date=booking_data.scheduled_date,
        notes=booking_data.notes,
        status=BookingStatus.PENDING
    )
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    return APIResponse(
        success=True,
        message="Booking created successfully",
        data={"booking_id": db_booking.id}
    )

@router.put("/{booking_id}", response_model=APIResponse)
async def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a booking"""
    
    booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Don't allow updates to completed bookings
    if booking.status == BookingStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update completed booking"
        )
    
    # Validate new scheduled date if provided
    if booking_update.scheduled_date and booking_update.scheduled_date <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking date must be in the future"
        )
    
    # Update booking fields
    update_data = booking_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(booking, field, value)
    
    db.commit()
    db.refresh(booking)
    
    return APIResponse(
        success=True,
        message="Booking updated successfully"
    )

@router.delete("/{booking_id}", response_model=APIResponse)
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel a booking"""
    
    booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Don't allow cancellation of completed bookings
    if booking.status == BookingStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel completed booking"
        )
    
    # Update status to cancelled
    booking.status = BookingStatus.CANCELLED
    db.commit()
    
    return APIResponse(
        success=True,
        message="Booking cancelled successfully"
    )

@router.get("/activity/{activity_id}/availability", response_model=List[datetime])
async def get_activity_availability(
    activity_id: int,
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db)
):
    """Get available time slots for an activity"""
    
    # Verify activity exists
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # For now, return simple availability (can be enhanced with complex scheduling)
    # This is a basic implementation - in practice, you'd have more sophisticated availability logic
    
    return APIResponse(
        success=True,
        message="Activity availability retrieved",
        data={
            "activity_id": activity_id,
            "note": "Availability logic to be implemented based on business rules"
        }
    )