"""Activity management routes for CRUD operations and AI suggestions."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from auth import get_current_active_user
from models import Activity, User
import schemas
from ai.suggestions import get_ai_suggestions
import math

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
async def list_activities(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title and summary"),
    skill_tags: Optional[List[str]] = Query(None, description="Filter by skill tags"),
    db: Session = Depends(get_db)
):
    """List activities with pagination and filtering."""
    query = db.query(Activity).filter(Activity.is_active == True)
    
    # Apply filters
    if category:
        query = query.filter(Activity.category == category)
    
    if search:
        search_filter = or_(
            Activity.title.ilike(f"%{search}%"),
            Activity.summary.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    if skill_tags:
        for tag in skill_tags:
            query = query.filter(Activity.skill_tags.contains([tag]))
    
    # Count total results
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    activities = query.offset(offset).limit(page_size).all()
    
    total_pages = math.ceil(total / page_size)
    
    return schemas.PaginatedResponse(
        data=[schemas.Activity.from_orm(activity) for activity in activities],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/{activity_id}", response_model=schemas.Activity)
async def get_activity(activity_id: str, db: Session = Depends(get_db)):
    """Get a specific activity by ID."""
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity

@router.post("/", response_model=schemas.SuccessResponse)
async def create_activity(
    activity: schemas.ActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new activity."""
    db_activity = Activity(
        **activity.dict(),
        creator_id=current_user.id
    )
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return schemas.SuccessResponse(
        data={"activity_id": db_activity.id},
        message="Activity created successfully"
    )

@router.put("/{activity_id}", response_model=schemas.SuccessResponse)
async def update_activity(
    activity_id: str,
    activity_update: schemas.ActivityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an existing activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user is the creator or has permission to edit
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this activity")
    
    # Update fields
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return schemas.SuccessResponse(
        data={"activity_id": activity.id},
        message="Activity updated successfully"
    )

@router.delete("/{activity_id}", response_model=schemas.SuccessResponse)
async def delete_activity(
    activity_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete (deactivate) an activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user is the creator or has permission to delete
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this activity")
    
    # Soft delete by setting is_active to False
    activity.is_active = False
    db.commit()
    
    return schemas.SuccessResponse(
        message="Activity deleted successfully"
    )

@router.get("/categories/list")
async def list_categories():
    """Get list of available activity categories."""
    categories = [
        {"id": "agri", "name": "Agriculture", "description": "Agricultural activities and farming"},
        {"id": "transfo", "name": "Transformation", "description": "Food transformation and processing"},
        {"id": "artisanat", "name": "Artisanat", "description": "Traditional crafts and handwork"},
        {"id": "nature", "name": "Nature", "description": "Environmental and nature-based activities"},
        {"id": "social", "name": "Social", "description": "Community and social activities"}
    ]
    
    return schemas.SuccessResponse(data=categories)

@router.post("/suggestions", response_model=schemas.SuggestionResponse)
async def get_suggestions(
    request: schemas.SuggestionRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered activity suggestions for the user."""
    # Use current user if no user_id specified
    user_id = request.user_id or current_user.id
    
    # Get user for suggestions
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get activities
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    
    # Get AI suggestions
    suggestions = await get_ai_suggestions(
        user=user,
        activities=activities,
        preferences=request.preferences,
        limit=request.limit
    )
    
    return suggestions