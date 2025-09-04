"""
Analytics API endpoints
"""
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.core.security import get_current_active_user
from app.models.models import (
    User, 
    Activity, 
    Booking, 
    AnalyticsEvent, 
    BookingStatus,
    ActivityCategory
)
from app.schemas.schemas import (
    AnalyticsEventCreate,
    APIResponse
)

router = APIRouter()

@router.post("/events", response_model=APIResponse)
async def track_event(
    event: AnalyticsEventCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Track an analytics event"""
    
    db_event = AnalyticsEvent(
        user_id=current_user.id,
        event_type=event.event_type,
        event_data=json.dumps(event.event_data) if event.event_data else None
    )
    
    db.add(db_event)
    db.commit()
    
    return APIResponse(
        success=True,
        message="Event tracked successfully"
    )

@router.get("/dashboard", response_model=APIResponse)
async def get_user_analytics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get analytics dashboard data for current user"""
    
    # Get user's booking statistics
    total_bookings = db.query(Booking).filter(Booking.user_id == current_user.id).count()
    completed_bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.status == BookingStatus.COMPLETED
    ).count()
    pending_bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.status == BookingStatus.PENDING
    ).count()
    
    # Get activities by category that user has booked
    category_stats = db.query(
        Activity.category,
        func.count(Booking.id).label('count')
    ).join(
        Booking, Activity.id == Booking.activity_id
    ).filter(
        Booking.user_id == current_user.id
    ).group_by(Activity.category).all()
    
    # Recent activity
    recent_bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.created_at.desc()).limit(5).all()
    
    return APIResponse(
        success=True,
        message="User analytics retrieved",
        data={
            "bookings": {
                "total": total_bookings,
                "completed": completed_bookings,
                "pending": pending_bookings,
                "cancelled": total_bookings - completed_bookings - pending_bookings
            },
            "categories": [
                {"category": stat.category, "count": stat.count}
                for stat in category_stats
            ],
            "recent_activities": [
                {
                    "booking_id": booking.id,
                    "activity_id": booking.activity_id,
                    "scheduled_date": booking.scheduled_date.isoformat(),
                    "status": booking.status
                }
                for booking in recent_bookings
            ]
        }
    )

@router.get("/global", response_model=APIResponse)
async def get_global_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get global platform analytics (admin view for future use)"""
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Total counts
    total_users = db.query(User).filter(User.is_active == True).count()
    total_activities = db.query(Activity).filter(Activity.is_active == True).count()
    total_bookings = db.query(Booking).filter(
        Booking.created_at >= start_date
    ).count()
    
    # Most popular activities
    popular_activities = db.query(
        Activity.title,
        func.count(Booking.id).label('booking_count')
    ).join(
        Booking, Activity.id == Booking.activity_id
    ).filter(
        Booking.created_at >= start_date
    ).group_by(
        Activity.id, Activity.title
    ).order_by(
        func.count(Booking.id).desc()
    ).limit(10).all()
    
    # Category distribution
    category_distribution = db.query(
        Activity.category,
        func.count(Booking.id).label('booking_count')
    ).join(
        Booking, Activity.id == Booking.activity_id
    ).filter(
        Booking.created_at >= start_date
    ).group_by(Activity.category).all()
    
    return APIResponse(
        success=True,
        message="Global analytics retrieved",
        data={
            "summary": {
                "total_users": total_users,
                "total_activities": total_activities,
                "total_bookings_period": total_bookings,
                "period_days": days
            },
            "popular_activities": [
                {"title": activity.title, "bookings": activity.booking_count}
                for activity in popular_activities
            ],
            "category_distribution": [
                {"category": cat.category, "bookings": cat.booking_count}
                for cat in category_distribution
            ]
        }
    )

@router.get("/trends", response_model=APIResponse)
async def get_booking_trends(
    days: int = Query(30, ge=7, le=90),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get booking trends over time"""
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Daily booking counts
    daily_bookings = db.query(
        func.date(Booking.created_at).label('date'),
        func.count(Booking.id).label('count')
    ).filter(
        Booking.created_at >= start_date,
        Booking.user_id == current_user.id
    ).group_by(
        func.date(Booking.created_at)
    ).order_by(
        func.date(Booking.created_at)
    ).all()
    
    return APIResponse(
        success=True,
        message="Booking trends retrieved",
        data={
            "daily_bookings": [
                {"date": booking.date.isoformat(), "count": booking.count}
                for booking in daily_bookings
            ],
            "period_days": days
        }
    )