"""
Activities API endpoints.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from sqlalchemy.orm import Session

from ...core.dependencies import standard_rate_limit, upload_rate_limit
from ...core.security import get_current_active_user, require_instructor
from ...db.session import get_db
from ...models.user import User
from ...models.activity import Activity, ActivitySubmission
from ...schemas.activity import (
    Activity as ActivitySchema,
    ActivityCreate, ActivityUpdate, ActivityFilter,
    ActivitySubmission as ActivitySubmissionSchema,
    ActivitySubmissionCreate, ActivitySubmissionUpdate, ActivitySubmissionReview,
    ActivitySuggestion
)
from ...services.openai import OpenAIService

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/", response_model=List[ActivitySchema])
@standard_rate_limit
async def list_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = Query(None),
    difficulty_level: Optional[int] = Query(None, ge=1, le=5),
    safety_level: Optional[int] = Query(None, ge=1, le=5),
    is_featured: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List activities with filtering."""
    
    query = db.query(Activity).filter(Activity.is_active == True)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if difficulty_level:
        query = query.filter(Activity.difficulty_level == difficulty_level)
    
    if safety_level:
        query = query.filter(Activity.safety_level == safety_level)
    
    if is_featured is not None:
        query = query.filter(Activity.is_featured == is_featured)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Activity.title.ilike(search_term) |
            Activity.summary.ilike(search_term) |
            Activity.description.ilike(search_term)
        )
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/suggestions", response_model=List[ActivitySuggestion])
@standard_rate_limit
async def get_activity_suggestions(
    limit: int = Query(5, ge=1, le=10),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized activity suggestions for the current user."""
    
    # Get available activities
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    
    if not activities:
        return []
    
    # Get AI suggestions
    openai_service = OpenAIService()
    suggestions = await openai_service.generate_activity_suggestions(
        current_user, activities, limit
    )
    
    return suggestions


@router.get("/{activity_id}", response_model=ActivitySchema)
@standard_rate_limit
async def get_activity(
    activity_id: UUID,
    db: Session = Depends(get_db)
):
    """Get activity by ID."""
    
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity


@router.post("/", response_model=ActivitySchema)
@standard_rate_limit
async def create_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    """Create new activity (instructor and above only)."""
    
    activity = Activity(
        **activity_data.dict(),
        created_by=current_user.id
    )
    
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return activity


@router.put("/{activity_id}", response_model=ActivitySchema)
@standard_rate_limit
async def update_activity(
    activity_id: UUID,
    activity_data: ActivityUpdate,
    current_user: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    """Update activity (instructor and above only)."""
    
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions (creator or moderator+)
    if (activity.created_by != current_user.id and 
        not current_user.is_moderator_or_above):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = activity_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}")
@standard_rate_limit
async def delete_activity(
    activity_id: UUID,
    current_user: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    """Delete activity (instructor and above only)."""
    
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check permissions (creator or moderator+)
    if (activity.created_by != current_user.id and 
        not current_user.is_moderator_or_above):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Soft delete by setting is_active to False
    activity.is_active = False
    db.commit()
    
    return {"message": "Activity deleted successfully"}


# Activity submissions
@router.get("/{activity_id}/submissions", response_model=List[ActivitySubmissionSchema])
@standard_rate_limit
async def list_activity_submissions(
    activity_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List submissions for an activity."""
    
    # Check if activity exists
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    query = db.query(ActivitySubmission).filter(
        ActivitySubmission.activity_id == activity_id
    )
    
    # Students can only see their own submissions
    if not current_user.is_instructor_or_above:
        query = query.filter(ActivitySubmission.user_id == current_user.id)
    
    submissions = query.all()
    return submissions


@router.post("/{activity_id}/submissions", response_model=ActivitySubmissionSchema)
@standard_rate_limit
async def create_submission(
    activity_id: UUID,
    submission_data: ActivitySubmissionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create new activity submission."""
    
    # Check if activity exists and is active
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Check if user already has a submission for this activity
    existing_submission = db.query(ActivitySubmission).filter(
        ActivitySubmission.user_id == current_user.id,
        ActivitySubmission.activity_id == activity_id
    ).first()
    
    if existing_submission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submission already exists for this activity"
        )
    
    submission = ActivitySubmission(
        user_id=current_user.id,
        activity_id=activity_id,
        **submission_data.dict(exclude={'activity_id'})
    )
    
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    return submission


@router.put("/submissions/{submission_id}", response_model=ActivitySubmissionSchema)
@standard_rate_limit
async def update_submission(
    submission_id: UUID,
    submission_data: ActivitySubmissionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update activity submission."""
    
    submission = db.query(ActivitySubmission).filter(
        ActivitySubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Check permissions (submission owner only)
    if submission.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = submission_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(submission, field, value)
    
    db.commit()
    db.refresh(submission)
    
    return submission


@router.post("/submissions/{submission_id}/review")
@standard_rate_limit
async def review_submission(
    submission_id: UUID,
    review_data: ActivitySubmissionReview,
    current_user: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    """Review activity submission (instructor and above only)."""
    
    submission = db.query(ActivitySubmission).filter(
        ActivitySubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Update review fields
    submission.score = review_data.score
    submission.feedback = review_data.feedback
    submission.reviewed_by = current_user.id
    submission.reviewed_at = datetime.utcnow()
    submission.status = "reviewed"
    
    db.commit()
    db.refresh(submission)
    
    return {"message": "Submission reviewed successfully"}


@router.post("/{activity_id}/upload", response_model=dict)
@upload_rate_limit
async def upload_activity_file(
    activity_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload file for activity submission."""
    
    # Check if activity exists
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Validate file type and size
    allowed_types = ["image/jpeg", "image/png", "image/gif", "application/pdf", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed"
        )
    
    # TODO: Implement actual file storage (S3, local storage, etc.)
    # For now, return a mock response
    file_path = f"uploads/{current_user.id}/{activity_id}/{file.filename}"
    
    return {
        "filename": file.filename,
        "file_path": file_path,
        "content_type": file.content_type,
        "message": "File uploaded successfully"
    }