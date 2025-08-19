"""Progress API routes."""

from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...api.deps import get_current_active_user, get_current_instructor_or_admin
from ...db.session import get_db
from ...models.progress import Progress
from ...models.user import User
from ...schemas.progress import (
    Progress as ProgressSchema,
    ProgressCreate,
    ProgressUpdate,
    ProgressWithDetails,
    UserProgress
)

router = APIRouter()


@router.get("/", response_model=List[ProgressWithDetails])
def read_progress_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Retrieve progress records."""
    query = db.query(Progress)
    
    # Students can only see their own progress
    if current_user.role == "student":
        query = query.filter(Progress.user_id == current_user.id)
    
    progress_records = query.offset(skip).limit(limit).all()
    return progress_records


@router.post("/", response_model=ProgressSchema)
def create_progress_record(
    progress_in: ProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create new progress record."""
    # Check if activity exists
    from ...models.activity import Activity
    activity = db.query(Activity).filter(Activity.id == progress_in.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Students can only create progress for themselves
    user_id = current_user.id
    if (current_user.role != "student" and 
        hasattr(progress_in, 'user_id') and 
        progress_in.user_id):
        user_id = progress_in.user_id
    
    # Check if progress record already exists
    existing_progress = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id,
            Progress.activity_id == progress_in.activity_id
        )
        .first()
    )
    if existing_progress:
        raise HTTPException(
            status_code=400,
            detail="Progress record already exists for this activity"
        )
    
    db_progress = Progress(
        user_id=user_id,
        **progress_in.dict()
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    
    return db_progress


@router.get("/user/{user_id}", response_model=UserProgress)
def get_user_progress(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get user progress summary."""
    # Students can only see their own progress
    if current_user.role == "student" and user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if user exists
    from ...models.user import User as UserModel
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user statistics
    progress_records = db.query(Progress).filter(Progress.user_id == user_id).all()
    total_bookings = len(user.bookings)
    completed_activities = len(progress_records)
    total_time_spent = sum(p.time_spent_minutes or 0 for p in progress_records)
    
    # Get unique skills
    skills_acquired = []
    for record in progress_records:
        skills_acquired.extend(record.skills_gained or [])
    skills_acquired = list(set(skills_acquired))
    
    # Get recent activities
    recent_activities = (
        db.query(Progress)
        .filter(Progress.user_id == user_id)
        .order_by(Progress.completed_at.desc())
        .limit(5)
        .all()
    )
    
    return {
        "user_id": user_id,
        "total_activities": total_bookings,
        "completed_activities": completed_activities,
        "total_time_spent": total_time_spent,
        "skills_acquired": skills_acquired,
        "recent_activities": recent_activities
    }


@router.get("/{progress_id}", response_model=ProgressWithDetails)
def read_progress_record(
    progress_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get progress record by ID."""
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress record not found")
    
    # Students can only see their own progress
    if current_user.role == "student" and progress.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return progress


@router.put("/{progress_id}", response_model=ProgressSchema)
def update_progress_record(
    progress_id: UUID,
    progress_update: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Update progress record (instructor/admin only)."""
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress record not found")
    
    progress_data = progress_update.dict(exclude_unset=True)
    for field, value in progress_data.items():
        setattr(progress, field, value)
    
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


@router.delete("/{progress_id}")
def delete_progress_record(
    progress_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin),
) -> Any:
    """Delete progress record (instructor/admin only)."""
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress record not found")
    
    db.delete(progress)
    db.commit()
    return {"message": "Progress record deleted successfully"}