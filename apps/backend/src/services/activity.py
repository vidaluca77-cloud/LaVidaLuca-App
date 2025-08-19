"""Activity service."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.activity import Activity, ActivityCategory
from ..schemas.activity import ActivityCreate, ActivityUpdate


class ActivityService:
    """Activity service."""

    @staticmethod
    def get_activity(db: Session, activity_id: UUID) -> Optional[Activity]:
        """Get activity by ID."""
        return db.query(Activity).filter(Activity.id == activity_id).first()

    @staticmethod
    def get_activity_by_slug(db: Session, slug: str) -> Optional[Activity]:
        """Get activity by slug."""
        return db.query(Activity).filter(Activity.slug == slug).first()

    @staticmethod
    def get_activities(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[ActivityCategory] = None,
        location_id: Optional[UUID] = None,
        difficulty_level: Optional[int] = None,
        is_active: bool = True
    ) -> List[Activity]:
        """Get activities with filters."""
        query = db.query(Activity).filter(Activity.is_active == is_active)
        
        if category:
            query = query.filter(Activity.category == category)
        if location_id:
            query = query.filter(Activity.location_id == location_id)
        if difficulty_level:
            query = query.filter(Activity.difficulty_level == difficulty_level)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_activity(db: Session, activity_create: ActivityCreate) -> Activity:
        """Create new activity."""
        db_activity = Activity(**activity_create.dict())
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity

    @staticmethod
    def update_activity(db: Session, activity: Activity, activity_update: ActivityUpdate) -> Activity:
        """Update activity."""
        activity_data = activity_update.dict(exclude_unset=True)
        for field, value in activity_data.items():
            setattr(activity, field, value)
        
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def delete_activity(db: Session, activity: Activity) -> None:
        """Soft delete activity."""
        activity.is_active = False
        db.add(activity)
        db.commit()

    @staticmethod
    def hard_delete_activity(db: Session, activity: Activity) -> None:
        """Hard delete activity."""
        db.delete(activity)
        db.commit()

    @staticmethod
    def search_activities(db: Session, query: str) -> List[Activity]:
        """Search activities by title, description, or skill tags."""
        search_term = f"%{query}%"
        return (
            db.query(Activity)
            .filter(
                Activity.is_active == True,
                (Activity.title.ilike(search_term)) |
                (Activity.description.ilike(search_term)) |
                (Activity.skill_tags.any(query))
            )
            .all()
        )

    @staticmethod
    def get_activities_by_category(db: Session, category: ActivityCategory) -> List[Activity]:
        """Get activities by category."""
        return (
            db.query(Activity)
            .filter(Activity.category == category, Activity.is_active == True)
            .all()
        )

    @staticmethod
    def get_activities_by_location(db: Session, location_id: UUID) -> List[Activity]:
        """Get activities by location."""
        return (
            db.query(Activity)
            .filter(Activity.location_id == location_id, Activity.is_active == True)
            .all()
        )

    @staticmethod
    def get_popular_activities(db: Session, limit: int = 10) -> List[Activity]:
        """Get popular activities based on booking count."""
        from ..models.booking import Booking
        
        # Get activities with most bookings
        popular_activities = (
            db.query(Activity)
            .join(Booking, Activity.id == Booking.activity_id)
            .filter(Activity.is_active == True)
            .group_by(Activity.id)
            .order_by(db.func.count(Booking.id).desc())
            .limit(limit)
            .all()
        )
        
        return popular_activities

    @staticmethod
    def get_activity_statistics(db: Session, activity: Activity) -> dict:
        """Get activity statistics."""
        from ..models.booking import Booking
        from ..models.progress import Progress
        
        total_bookings = len(activity.bookings)
        completed_bookings = len([b for b in activity.bookings if b.status == "completed"])
        progress_records = len(activity.progress_records)
        
        # Calculate average rating
        ratings = [p.rating for p in activity.progress_records if p.rating]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        return {
            "total_bookings": total_bookings,
            "completed_bookings": completed_bookings,
            "progress_records": progress_records,
            "average_rating": round(avg_rating, 2),
            "completion_rate": round((completed_bookings / total_bookings * 100) if total_bookings > 0 else 0, 2)
        }