from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...api.deps import get_current_active_user
from ...models.models import User, Activity
from ...schemas.schemas import ActivityCreate, ActivityUpdate, Activity as ActivitySchema


router = APIRouter()


@router.get(
    "/",
    response_model=List[ActivitySchema],
    summary="Get list of activities",
    description="""
    Retrieve a paginated list of educational activities with optional filtering.
    
    This endpoint returns activities based on the specified criteria. By default,
    only published activities are returned to ensure content quality.
    
    **Filtering Options:**
    - **Category**: Filter by activity category (agriculture, technology, etc.)
    - **Difficulty**: Filter by difficulty level (beginner, intermediate, advanced)
    - **Published Only**: Include only published activities (default: true)
    
    **Pagination:**
    - Use `skip` to offset results for pagination
    - Use `limit` to control the number of results (max: 100)
    
    **Use Cases:**
    - Browse available activities for learning
    - Find activities by specific category or difficulty
    - Implement pagination for activity lists
    """,
    responses={
        200: {
            "description": "List of activities successfully retrieved",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "Introduction to Sustainable Farming",
                            "description": "Learn the basics of sustainable farming practices...",
                            "category": "agriculture",
                            "difficulty_level": "beginner",
                            "duration_minutes": 120,
                            "location": "School Farm",
                            "equipment_needed": "Notebook, pen, soil samples",
                            "learning_objectives": "Understand sustainable farming principles...",
                            "is_published": True,
                            "creator_id": 1,
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-20T14:45:00Z"
                        }
                    ]
                }
            }
        },
        422: {
            "description": "Invalid query parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["query", "limit"],
                                "msg": "ensure this value is less than or equal to 100",
                                "type": "value_error.number.not_le"
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=["activities"]
)
def get_activities(
    skip: int = Query(0, ge=0, description="Number of activities to skip for pagination"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of activities to return"),
    category: str = Query(None, description="Filter by activity category"),
    difficulty: str = Query(None, description="Filter by difficulty level"),
    published_only: bool = Query(True, description="Include only published activities"),
    db: Session = Depends(get_db)
):
    """Get a paginated list of activities with optional filtering."""
    query = db.query(Activity)
    
    if published_only:
        query = query.filter(Activity.is_published == True)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if difficulty:
        query = query.filter(Activity.difficulty_level == difficulty)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get(
    "/{activity_id}",
    response_model=ActivitySchema,
    summary="Get activity by ID",
    description="""
    Retrieve detailed information about a specific activity by its ID.
    
    This endpoint returns complete activity information including all metadata,
    learning objectives, equipment requirements, and timestamps.
    
    **Use Cases:**
    - View detailed activity information
    - Get activity data for editing (if user is the creator)
    - Display activity details in the UI
    """,
    responses={
        200: {
            "description": "Activity details successfully retrieved",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Introduction to Sustainable Farming",
                        "description": "Learn the basics of sustainable farming practices including crop rotation, organic fertilizers, and water conservation techniques.",
                        "category": "agriculture",
                        "difficulty_level": "beginner",
                        "duration_minutes": 120,
                        "location": "School Farm",
                        "equipment_needed": "Notebook, pen, soil samples",
                        "learning_objectives": "Understand sustainable farming principles, identify organic fertilizers, practice water conservation",
                        "is_published": True,
                        "creator_id": 1,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-20T14:45:00Z"
                    }
                }
            }
        },
        404: {
            "description": "Activity not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Activity not found"
                    }
                }
            }
        }
    },
    tags=["activities"]
)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post(
    "/",
    response_model=ActivitySchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new activity",
    description="""
    Create a new educational activity in the system.
    
    This endpoint allows authenticated users to create new learning activities
    with comprehensive metadata including objectives, equipment, and categorization.
    
    **Authentication Required:**
    - Must be logged in with valid JWT token
    - Activity will be associated with the current user as creator
    
    **Activity Information:**
    - Title and description are required
    - Category must be one of: agriculture, technology, environment, business, community
    - Difficulty level: beginner, intermediate, or advanced
    - Optional: duration, location, equipment, learning objectives
    
    **Publishing:**
    - Activities can be created as drafts (is_published: false)
    - Published activities are visible to all users
    """,
    responses={
        201: {
            "description": "Activity successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Introduction to Sustainable Farming",
                        "description": "Learn the basics of sustainable farming practices...",
                        "category": "agriculture",
                        "difficulty_level": "beginner",
                        "duration_minutes": 120,
                        "location": "School Farm",
                        "equipment_needed": "Notebook, pen, soil samples",
                        "learning_objectives": "Understand sustainable farming principles...",
                        "is_published": True,
                        "creator_id": 1,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": None
                    }
                }
            }
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "title"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=["activities"]
)
def create_activity(
    activity: ActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new educational activity."""
    db_activity = Activity(**activity.dict(), creator_id=current_user.id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@router.put(
    "/{activity_id}",
    response_model=ActivitySchema,
    summary="Update an existing activity",
    description="""
    Update an existing activity with new information.
    
    This endpoint allows activity creators (and superusers) to modify
    existing activities with partial or complete updates.
    
    **Authorization:**
    - Must be the activity creator OR a superuser
    - Authentication required with valid JWT token
    
    **Update Behavior:**
    - Only provided fields will be updated (partial updates supported)
    - Updated timestamp will be automatically set
    - All fields are optional for updates
    
    **Use Cases:**
    - Fix typos or improve descriptions
    - Update learning objectives or equipment requirements
    - Publish draft activities
    - Modify activity categorization
    """,
    responses={
        200: {
            "description": "Activity successfully updated",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Advanced Sustainable Farming Techniques",
                        "description": "Learn advanced sustainable farming practices...",
                        "category": "agriculture",
                        "difficulty_level": "intermediate",
                        "duration_minutes": 180,
                        "location": "School Farm",
                        "equipment_needed": "Notebook, pen, soil samples, pH meter",
                        "learning_objectives": "Master sustainable farming principles...",
                        "is_published": True,
                        "creator_id": 1,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-22T16:20:00Z"
                    }
                }
            }
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        },
        403: {
            "description": "Insufficient permissions",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not enough permissions"
                    }
                }
            }
        },
        404: {
            "description": "Activity not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Activity not found"
                    }
                }
            }
        }
    },
    tags=["activities"]
)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an existing activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user owns the activity or is superuser
    if activity.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update fields
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    return activity


@router.delete(
    "/{activity_id}",
    summary="Delete an activity",
    description="""
    Permanently delete an activity from the system.
    
    This endpoint allows activity creators (and superusers) to remove
    activities from the platform. This operation cannot be undone.
    
    **Authorization:**
    - Must be the activity creator OR a superuser
    - Authentication required with valid JWT token
    
    **Important Notes:**
    - This operation is permanent and cannot be undone
    - All associated suggestions will also be removed
    - Consider unpublishing instead of deleting if you want to preserve data
    
    **Use Cases:**
    - Remove duplicate or inappropriate content
    - Clean up test activities
    - Remove outdated or incorrect information
    """,
    responses={
        200: {
            "description": "Activity successfully deleted",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Activity deleted successfully"
                    }
                }
            }
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        },
        403: {
            "description": "Insufficient permissions",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not enough permissions"
                    }
                }
            }
        },
        404: {
            "description": "Activity not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Activity not found"
                    }
                }
            }
        }
    },
    tags=["activities"]
)
def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an activity permanently."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user owns the activity or is superuser
    if activity.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}


@router.get(
    "/categories/",
    response_model=List[str],
    summary="Get available activity categories",
    description="""
    Retrieve a list of all activity categories currently used in the system.
    
    This endpoint returns the distinct categories from existing activities,
    which can be used for filtering and categorization purposes.
    
    **Use Cases:**
    - Populate category filters in the UI
    - Validate category input
    - Show available categories to users
    
    **Categories Include:**
    - Agriculture: Farming techniques and agricultural practices
    - Technology: Modern farming technology and digital tools
    - Environment: Sustainable practices and environmental conservation
    - Business: Agricultural business and entrepreneurship
    - Community: Social skills and community engagement
    """,
    responses={
        200: {
            "description": "List of categories successfully retrieved",
            "content": {
                "application/json": {
                    "example": ["agriculture", "technology", "environment", "business", "community"]
                }
            }
        }
    },
    tags=["activities"]
)
def get_activity_categories(db: Session = Depends(get_db)):
    """Get list of all available activity categories."""
    categories = db.query(Activity.category).distinct().all()
    return [category[0] for category in categories if category[0]]