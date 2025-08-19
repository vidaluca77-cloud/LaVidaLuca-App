from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models import Activity, ActivityCreate, ActivityUpdate, User
from app.auth.auth import get_current_active_user
from app.database import get_supabase_client
import uuid

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("/", response_model=List[Activity])
async def get_activities(
    category: Optional[str] = Query(None, description="Filter by category"),
    skill_tag: Optional[str] = Query(None, description="Filter by skill tag"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all activities with optional filtering."""
    supabase = get_supabase_client()
    
    try:
        query = supabase.table("activities").select("*")
        
        if category:
            query = query.eq("category", category)
        
        if skill_tag:
            query = query.contains("skill_tags", [skill_tag])
        
        response = query.range(offset, offset + limit - 1).execute()
        
        return [Activity(**activity) for activity in response.data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch activities: {str(e)}"
        )

@router.get("/{activity_id}", response_model=Activity)
async def get_activity(activity_id: str):
    """Get a specific activity by ID."""
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("activities").select("*").eq("id", activity_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found"
            )
        
        return Activity(**response.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch activity: {str(e)}"
        )

@router.post("/", response_model=Activity, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new activity (admin only)."""
    supabase = get_supabase_client()
    
    # Check if slug already exists
    try:
        existing = supabase.table("activities").select("id").eq("slug", activity_data.slug).execute()
        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Activity with this slug already exists"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check existing activity: {str(e)}"
        )
    
    activity_dict = {
        "id": str(uuid.uuid4()),
        **activity_data.dict()
    }
    
    try:
        response = supabase.table("activities").insert(activity_dict).execute()
        
        if response.data:
            return Activity(**response.data[0])
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create activity"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.put("/{activity_id}", response_model=Activity)
async def update_activity(
    activity_id: str,
    activity_data: ActivityUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing activity (admin only)."""
    supabase = get_supabase_client()
    
    # Check if activity exists
    try:
        existing = supabase.table("activities").select("*").eq("id", activity_id).execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check activity: {str(e)}"
        )
    
    # Update only provided fields
    update_data = {k: v for k, v in activity_data.dict().items() if v is not None}
    
    try:
        response = supabase.table("activities").update(update_data).eq("id", activity_id).execute()
        
        if response.data:
            return Activity(**response.data[0])
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update activity"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete an activity (admin only)."""
    supabase = get_supabase_client()
    
    try:
        # Check if activity exists
        existing = supabase.table("activities").select("id").eq("id", activity_id).execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found"
            )
        
        # Delete the activity
        supabase.table("activities").delete().eq("id", activity_id).execute()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete activity: {str(e)}"
        )