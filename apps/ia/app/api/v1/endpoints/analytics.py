from typing import Dict, Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.activity import Activity, ActivityCategory
from app.models.booking import Booking, BookingStatus

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get dashboard statistics for the current user"""
    
    # User's booking stats
    user_bookings = await db.execute(
        select(func.count(Booking.id))
        .where(Booking.user_id == current_user.id)
    )
    total_bookings = user_bookings.scalar()
    
    completed_bookings = await db.execute(
        select(func.count(Booking.id))
        .where(
            and_(
                Booking.user_id == current_user.id,
                Booking.status == BookingStatus.COMPLETED
            )
        )
    )
    completed_count = completed_bookings.scalar()
    
    pending_bookings = await db.execute(
        select(func.count(Booking.id))
        .where(
            and_(
                Booking.user_id == current_user.id,
                Booking.status == BookingStatus.PENDING
            )
        )
    )
    pending_count = pending_bookings.scalar()
    
    # User's activity categories
    category_stats = await db.execute(
        select(Activity.category, func.count(Booking.id))
        .join(Booking, Activity.id == Booking.activity_id)
        .where(Booking.user_id == current_user.id)
        .group_by(Activity.category)
    )
    categories = {category: count for category, count in category_stats.fetchall()}
    
    return {
        "user": {
            "total_bookings": total_bookings,
            "completed_bookings": completed_count,
            "pending_bookings": pending_count,
            "category_participation": categories
        }
    }


@router.get("/activities/stats")
async def get_activity_stats(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get activity statistics for the specified period"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Most popular activities
    popular_activities = await db.execute(
        select(Activity.title, func.count(Booking.id).label('booking_count'))
        .join(Booking, Activity.id == Booking.activity_id)
        .where(Booking.created_at >= start_date)
        .group_by(Activity.id, Activity.title)
        .order_by(func.count(Booking.id).desc())
        .limit(10)
    )
    popular = [
        {"activity": title, "bookings": count}
        for title, count in popular_activities.fetchall()
    ]
    
    # Category distribution
    category_distribution = await db.execute(
        select(Activity.category, func.count(Booking.id))
        .join(Booking, Activity.id == Booking.activity_id)
        .where(Booking.created_at >= start_date)
        .group_by(Activity.category)
    )
    categories = {
        category.value: count
        for category, count in category_distribution.fetchall()
    }
    
    # Total activities and bookings
    total_activities = await db.execute(
        select(func.count(Activity.id))
        .where(Activity.is_active == True)
    )
    
    total_bookings_period = await db.execute(
        select(func.count(Booking.id))
        .where(Booking.created_at >= start_date)
    )
    
    return {
        "period_days": days,
        "total_activities": total_activities.scalar(),
        "total_bookings_period": total_bookings_period.scalar(),
        "popular_activities": popular,
        "category_distribution": categories
    }


@router.get("/bookings/trends")
async def get_booking_trends(
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get booking trends over time"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily booking counts
    daily_bookings = await db.execute(
        select(
            func.date(Booking.created_at).label('date'),
            func.count(Booking.id).label('count')
        )
        .where(Booking.created_at >= start_date)
        .group_by(func.date(Booking.created_at))
        .order_by(func.date(Booking.created_at))
    )
    
    trends = [
        {
            "date": date.isoformat(),
            "bookings": count
        }
        for date, count in daily_bookings.fetchall()
    ]
    
    return trends


@router.get("/skills/progress")
async def get_skills_progress(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get user's skill progression based on completed activities"""
    
    # Get completed activities and their skill tags
    completed_activities = await db.execute(
        select(Activity.skill_tags)
        .join(Booking, Activity.id == Booking.activity_id)
        .where(
            and_(
                Booking.user_id == current_user.id,
                Booking.status == BookingStatus.COMPLETED
            )
        )
    )
    
    # Count skill occurrences
    skill_counts = {}
    for (skill_tags,) in completed_activities.fetchall():
        if skill_tags:
            for skill in skill_tags:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    # User's declared skills
    user_skills = current_user.skills or []
    
    return {
        "declared_skills": user_skills,
        "practiced_skills": skill_counts,
        "new_skills_acquired": len(set(skill_counts.keys()) - set(user_skills)),
        "total_skill_practices": sum(skill_counts.values())
    }