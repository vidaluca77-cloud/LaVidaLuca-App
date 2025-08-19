from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.booking import Booking, BookingStatus
from app.models.activity import Activity
from app.schemas.booking import (
    Booking as BookingSchema,
    BookingCreate,
    BookingUpdate,
    BookingWithDetails
)

router = APIRouter()


@router.get("/", response_model=List[BookingWithDetails])
async def list_my_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[BookingStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """List current user's bookings"""
    query = (
        select(Booking)
        .options(selectinload(Booking.activity))
        .where(Booking.user_id == current_user.id)
    )
    
    if status:
        query = query.where(Booking.status == status)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    bookings = result.scalars().all()
    
    return bookings


@router.get("/{booking_id}", response_model=BookingWithDetails)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific booking"""
    result = await db.execute(
        select(Booking)
        .options(selectinload(Booking.activity))
        .where(
            and_(
                Booking.id == booking_id,
                Booking.user_id == current_user.id
            )
        )
    )
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return booking


@router.post("/", response_model=BookingSchema)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new booking"""
    # Verify activity exists
    result = await db.execute(select(Activity).where(Activity.id == booking_data.activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity or not activity.is_active:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check for conflicting bookings (same user, same time)
    existing_booking = await db.execute(
        select(Booking).where(
            and_(
                Booking.user_id == current_user.id,
                Booking.scheduled_date == booking_data.scheduled_date,
                Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
            )
        )
    )
    
    if existing_booking.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="You already have a booking at this time"
        )
    
    # Create booking
    db_booking = Booking(
        user_id=current_user.id,
        activity_id=booking_data.activity_id,
        scheduled_date=booking_data.scheduled_date,
        participants_count=booking_data.participants_count,
        user_notes=booking_data.user_notes,
        status=BookingStatus.PENDING
    )
    
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    
    return db_booking


@router.put("/{booking_id}", response_model=BookingSchema)
async def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a booking"""
    result = await db.execute(
        select(Booking).where(
            and_(
                Booking.id == booking_id,
                Booking.user_id == current_user.id
            )
        )
    )
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Only allow updates if booking is pending or confirmed
    if booking.status in [BookingStatus.CANCELLED, BookingStatus.COMPLETED]:
        raise HTTPException(
            status_code=400,
            detail="Cannot update cancelled or completed bookings"
        )
    
    # Update booking fields
    for field, value in booking_update.dict(exclude_unset=True).items():
        if field in ["admin_notes", "completion_feedback", "rating"]:
            # These fields can only be updated by admins
            # TODO: Add admin role check
            continue
        setattr(booking, field, value)
    
    await db.commit()
    await db.refresh(booking)
    
    return booking


@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Cancel a booking"""
    result = await db.execute(
        select(Booking).where(
            and_(
                Booking.id == booking_id,
                Booking.user_id == current_user.id
            )
        )
    )
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status == BookingStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel completed bookings"
        )
    
    booking.status = BookingStatus.CANCELLED
    await db.commit()
    
    return {"message": "Booking cancelled successfully"}


@router.get("/activity/{activity_id}/availability")
async def get_activity_availability(
    activity_id: int,
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get availability for an activity in a date range"""
    # Verify activity exists
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Get existing bookings in date range
    result = await db.execute(
        select(Booking).where(
            and_(
                Booking.activity_id == activity_id,
                Booking.scheduled_date >= start_date,
                Booking.scheduled_date <= end_date,
                Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
            )
        )
    )
    bookings = result.scalars().all()
    
    # TODO: Generate availability slots based on activity schedule
    # For now, return basic info
    occupied_slots = [booking.scheduled_date.isoformat() for booking in bookings]
    
    return {
        "activity_id": activity_id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "max_participants": activity.max_participants,
        "occupied_slots": occupied_slots
    }