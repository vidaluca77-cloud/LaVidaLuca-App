from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from app.core.models import Activity, ActivitySession, ActivityRegistration, User
from app.schemas.schemas import (
    ActivityCreate, ActivityUpdate, ActivitySessionCreate, ActivitySessionUpdate,
    ActivityRegistrationCreate, ActivityRegistrationUpdate, ActivityCategory
)

class ActivityService:
    def __init__(self, db: Session):
        self.db = db

    def get_activity(self, activity_id: int) -> Optional[Activity]:
        """Get activity by ID"""
        return self.db.query(Activity).filter(Activity.id == activity_id).first()

    def get_activity_by_slug(self, slug: str) -> Optional[Activity]:
        """Get activity by slug"""
        return self.db.query(Activity).filter(Activity.slug == slug).first()

    def get_activities(
        self, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[ActivityCategory] = None,
        requires_mfr: Optional[bool] = None,
        is_active: bool = True
    ) -> List[Activity]:
        """Get list of activities with filters"""
        query = self.db.query(Activity)
        
        if is_active is not None:
            query = query.filter(Activity.is_active == is_active)
        
        if category:
            query = query.filter(Activity.category == category.value)
            
        if requires_mfr is not None:
            query = query.filter(Activity.requires_mfr == requires_mfr)

        return query.offset(skip).limit(limit).all()

    def create_activity(self, activity_create: ActivityCreate) -> Activity:
        """Create new activity"""
        # Check if slug already exists
        if self.get_activity_by_slug(activity_create.slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Activity slug already exists"
            )

        db_activity = Activity(**activity_create.dict())
        self.db.add(db_activity)
        self.db.commit()
        self.db.refresh(db_activity)
        return db_activity

    def update_activity(self, activity_id: int, activity_update: ActivityUpdate) -> Optional[Activity]:
        """Update activity"""
        db_activity = self.get_activity(activity_id)
        if not db_activity:
            return None

        update_data = activity_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_activity, field, value)

        self.db.commit()
        self.db.refresh(db_activity)
        return db_activity

    def delete_activity(self, activity_id: int) -> bool:
        """Soft delete activity (mark as inactive)"""
        db_activity = self.get_activity(activity_id)
        if not db_activity:
            return False

        db_activity.is_active = False
        self.db.commit()
        return True

    def get_recommended_activities(self, user: User, limit: int = 10) -> List[dict]:
        """Get recommended activities for user based on profile"""
        # Get user profile
        from app.services.user_service import UserService
        user_service = UserService(self.db)
        profile = user_service.get_user_profile(user.id)
        
        activities = self.get_activities(limit=100, is_active=True)
        recommendations = []
        
        for activity in activities:
            score = 0
            reasons = []
            
            # Check if activity requires MFR status
            if activity.requires_mfr and not user.is_mfr_student:
                continue
            
            if profile:
                # Skills matching
                if profile.skills:
                    common_skills = set(activity.skill_tags) & set(profile.skills)
                    if common_skills:
                        score += len(common_skills) * 15
                        reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
                
                # Category preferences
                if profile.preferences and activity.category in profile.preferences:
                    score += 25
                    reasons.append(f"Catégorie préférée : {activity.category}")
                
                # Experience level
                if profile.experience_level == "beginner" and activity.safety_level <= 2:
                    score += 10
                    reasons.append("Adapté aux débutants")
                elif profile.experience_level == "advanced":
                    score += 5
            
            # Duration (shorter activities get bonus for beginners)
            if activity.duration_min <= 90:
                score += 10
                reasons.append("Durée adaptée pour débuter")
            
            # Safety level
            if activity.safety_level <= 2:
                score += 10
                if activity.safety_level == 1:
                    reasons.append("Activité sans risque particulier")
            
            if score > 0:
                recommendations.append({
                    "activity": activity,
                    "score": score,
                    "reasons": reasons
                })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        serialized_recommendations = []
        for rec in recommendations[:limit]:
            serialized_recommendations.append({
                "activity": {
                    "id": rec["activity"].id,
                    "slug": rec["activity"].slug,
                    "title": rec["activity"].title,
                    "category": rec["activity"].category,
                    "summary": rec["activity"].summary,
                    "description": rec["activity"].description,
                    "duration_min": rec["activity"].duration_min,
                    "safety_level": rec["activity"].safety_level,
                    "max_participants": rec["activity"].max_participants,
                    "min_age": rec["activity"].min_age,
                    "requires_mfr": rec["activity"].requires_mfr,
                    "skill_tags": rec["activity"].skill_tags,
                    "seasonality": rec["activity"].seasonality,
                    "materials": rec["activity"].materials,
                    "is_active": rec["activity"].is_active,
                    "created_at": rec["activity"].created_at,
                    "updated_at": rec["activity"].updated_at
                },
                "score": rec["score"],
                "reasons": rec["reasons"]
            })
        return serialized_recommendations

class ActivitySessionService:
    def __init__(self, db: Session):
        self.db = db

    def get_session(self, session_id: int) -> Optional[ActivitySession]:
        """Get session by ID"""
        return self.db.query(ActivitySession).filter(ActivitySession.id == session_id).first()

    def get_sessions_for_activity(self, activity_id: int) -> List[ActivitySession]:
        """Get all sessions for an activity"""
        return self.db.query(ActivitySession).filter(
            ActivitySession.activity_id == activity_id
        ).order_by(ActivitySession.start_date).all()

    def get_sessions(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[ActivitySession]:
        """Get list of sessions"""
        query = self.db.query(ActivitySession)
        
        if status:
            query = query.filter(ActivitySession.status == status)

        return query.order_by(ActivitySession.start_date).offset(skip).limit(limit).all()

    def create_session(self, session_create: ActivitySessionCreate) -> ActivitySession:
        """Create new session"""
        # Validate activity exists
        activity_service = ActivityService(self.db)
        activity = activity_service.get_activity(session_create.activity_id)
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found"
            )

        db_session = ActivitySession(**session_create.dict())
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def update_session(self, session_id: int, session_update: ActivitySessionUpdate) -> Optional[ActivitySession]:
        """Update session"""
        db_session = self.get_session(session_id)
        if not db_session:
            return None

        update_data = session_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_session, field, value)

        self.db.commit()
        self.db.refresh(db_session)
        return db_session

class ActivityRegistrationService:
    def __init__(self, db: Session):
        self.db = db

    def get_registration(self, registration_id: int) -> Optional[ActivityRegistration]:
        """Get registration by ID"""
        return self.db.query(ActivityRegistration).filter(
            ActivityRegistration.id == registration_id
        ).first()

    def get_user_registrations(self, user_id: int) -> List[ActivityRegistration]:
        """Get all registrations for a user"""
        return self.db.query(ActivityRegistration).filter(
            ActivityRegistration.user_id == user_id
        ).order_by(ActivityRegistration.registration_date.desc()).all()

    def get_activity_registrations(self, activity_id: int) -> List[ActivityRegistration]:
        """Get all registrations for an activity"""
        return self.db.query(ActivityRegistration).filter(
            ActivityRegistration.activity_id == activity_id
        ).order_by(ActivityRegistration.registration_date.desc()).all()

    def create_registration(
        self, 
        user_id: int, 
        registration_create: ActivityRegistrationCreate
    ) -> ActivityRegistration:
        """Create new registration"""
        # Check if user already registered for this activity
        existing = self.db.query(ActivityRegistration).filter(
            and_(
                ActivityRegistration.user_id == user_id,
                ActivityRegistration.activity_id == registration_create.activity_id,
                ActivityRegistration.status.in_(["pending", "confirmed"])
            )
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already registered for this activity"
            )

        # Validate activity exists
        activity_service = ActivityService(self.db)
        activity = activity_service.get_activity(registration_create.activity_id)
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found"
            )

        # Check if session exists (if provided)
        if registration_create.session_id:
            session_service = ActivitySessionService(self.db)
            session = session_service.get_session(registration_create.session_id)
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Session not found"
                )
            
            # Check if session is full
            if session.current_participants >= session.max_participants:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Session is full"
                )

        db_registration = ActivityRegistration(
            user_id=user_id,
            **registration_create.dict()
        )
        
        self.db.add(db_registration)
        self.db.commit()
        self.db.refresh(db_registration)
        
        # Update session participant count if applicable
        if registration_create.session_id:
            session = session_service.get_session(registration_create.session_id)
            session.current_participants += 1
            if session.current_participants >= session.max_participants:
                session.status = "full"
            self.db.commit()
        
        return db_registration

    def update_registration(
        self, 
        registration_id: int, 
        registration_update: ActivityRegistrationUpdate
    ) -> Optional[ActivityRegistration]:
        """Update registration"""
        db_registration = self.get_registration(registration_id)
        if not db_registration:
            return None

        old_status = db_registration.status
        update_data = registration_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_registration, field, value)

        self.db.commit()
        self.db.refresh(db_registration)
        
        # Update session participant count if status changed
        if (registration_update.status and 
            old_status != registration_update.status and 
            db_registration.session_id):
            
            session_service = ActivitySessionService(self.db)
            session = session_service.get_session(db_registration.session_id)
            
            if old_status in ["pending", "confirmed"] and registration_update.status == "cancelled":
                session.current_participants = max(0, session.current_participants - 1)
                if session.status == "full":
                    session.status = "open"
            elif old_status == "cancelled" and registration_update.status in ["pending", "confirmed"]:
                session.current_participants += 1
                if session.current_participants >= session.max_participants:
                    session.status = "full"
            
            self.db.commit()
        
        return db_registration