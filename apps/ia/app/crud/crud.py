import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.models import User, Activity, Application
from app.schemas.schemas import UserCreate, UserUpdate, ActivityCreate, ActivityUpdate, ApplicationCreate, ApplicationUpdate
from app.core.security import get_password_hash, verify_password

# User CRUD
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        user = get_user_by_email(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Activity CRUD
def get_activity(db: Session, activity_id: int) -> Optional[Activity]:
    return db.query(Activity).filter(Activity.id == activity_id).first()

def get_activity_by_slug(db: Session, slug: str) -> Optional[Activity]:
    return db.query(Activity).filter(Activity.slug == slug).first()

def get_activities(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[Activity]:
    query = db.query(Activity).filter(Activity.is_active == True)
    if category:
        query = query.filter(Activity.category == category)
    return query.offset(skip).limit(limit).all()

def create_activity(db: Session, activity: ActivityCreate) -> Activity:
    db_activity = Activity(
        slug=activity.slug,
        title=activity.title,
        category=activity.category,
        summary=activity.summary,
        description=activity.description,
        duration_min=activity.duration_min,
        skill_tags=json.dumps(activity.skill_tags),
        seasonality=json.dumps(activity.seasonality),
        safety_level=activity.safety_level,
        materials=json.dumps(activity.materials),
        is_active=activity.is_active
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def update_activity(db: Session, activity_id: int, activity_update: ActivityUpdate) -> Optional[Activity]:
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return None
    
    update_data = activity_update.model_dump(exclude_unset=True)
    
    # Convert lists to JSON strings for storage
    for field in ["skill_tags", "seasonality", "materials"]:
        if field in update_data:
            update_data[field] = json.dumps(update_data[field])
    
    for field, value in update_data.items():
        setattr(db_activity, field, value)
    
    db.commit()
    db.refresh(db_activity)
    return db_activity

# Application CRUD
def get_application(db: Session, application_id: int) -> Optional[Application]:
    return db.query(Application).filter(Application.id == application_id).first()

def get_applications(db: Session, skip: int = 0, limit: int = 100, user_id: Optional[int] = None) -> List[Application]:
    query = db.query(Application)
    if user_id:
        query = query.filter(Application.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def create_application(db: Session, application: ApplicationCreate, user_id: int) -> Application:
    db_application = Application(
        user_id=user_id,
        activity_id=application.activity_id,
        message=application.message,
        status="pending"
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def update_application(db: Session, application_id: int, application_update: ApplicationUpdate) -> Optional[Application]:
    db_application = get_application(db, application_id)
    if not db_application:
        return None
    
    update_data = application_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_application, field, value)
    
    db.commit()
    db.refresh(db_application)
    return db_application