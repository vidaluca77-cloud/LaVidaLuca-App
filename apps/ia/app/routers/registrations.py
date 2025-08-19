from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models import Registration, RegistrationCreate, RegistrationUpdate, User, Activity
from app.auth.auth import get_current_active_user
from app.database import get_supabase_client
import uuid

router = APIRouter(prefix="/registrations", tags=["registrations"])

@router.get("/", response_model=List[Registration])
async def get_user_registrations(
    current_user: User = Depends(get_current_active_user),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get current user's registrations."""
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("registrations").select(
            "*, activities(*)"
        ).eq("user_id", current_user.id).range(offset, offset + limit - 1).execute()
        
        registrations = []
        for reg_data in response.data:
            registration = Registration(**reg_data)
            if reg_data.get("activities"):
                registration.activity = Activity(**reg_data["activities"])
            registrations.append(registration)
        
        return registrations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch registrations: {str(e)}"
        )

@router.get("/{registration_id}", response_model=Registration)
async def get_registration(
    registration_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific registration by ID."""
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("registrations").select(
            "*, activities(*)"
        ).eq("id", registration_id).eq("user_id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )
        
        reg_data = response.data[0]
        registration = Registration(**reg_data)
        if reg_data.get("activities"):
            registration.activity = Activity(**reg_data["activities"])
        
        return registration
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch registration: {str(e)}"
        )

@router.post("/", response_model=Registration, status_code=status.HTTP_201_CREATED)
async def create_registration(
    registration_data: RegistrationCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new registration for an activity."""
    supabase = get_supabase_client()
    
    # Check if activity exists
    try:
        activity_response = supabase.table("activities").select("*").eq("id", registration_data.activity_id).execute()
        if not activity_response.data:
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
    
    # Check if user already registered for this activity
    try:
        existing = supabase.table("registrations").select("id").eq(
            "user_id", current_user.id
        ).eq("activity_id", registration_data.activity_id).execute()
        
        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already registered for this activity"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check existing registration: {str(e)}"
        )
    
    registration_dict = {
        "id": str(uuid.uuid4()),
        "user_id": current_user.id,
        **registration_data.dict()
    }
    
    try:
        response = supabase.table("registrations").insert(registration_dict).execute()
        
        if response.data:
            # Fetch the registration with activity data
            full_response = supabase.table("registrations").select(
                "*, activities(*)"
            ).eq("id", response.data[0]["id"]).execute()
            
            reg_data = full_response.data[0]
            registration = Registration(**reg_data)
            if reg_data.get("activities"):
                registration.activity = Activity(**reg_data["activities"])
            
            return registration
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create registration"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.put("/{registration_id}", response_model=Registration)
async def update_registration(
    registration_id: str,
    registration_data: RegistrationUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing registration."""
    supabase = get_supabase_client()
    
    # Check if registration exists and belongs to user
    try:
        existing = supabase.table("registrations").select("*").eq(
            "id", registration_id
        ).eq("user_id", current_user.id).execute()
        
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check registration: {str(e)}"
        )
    
    # Update only provided fields
    update_data = {k: v for k, v in registration_data.dict().items() if v is not None}
    
    try:
        response = supabase.table("registrations").update(update_data).eq("id", registration_id).execute()
        
        if response.data:
            # Fetch the updated registration with activity data
            full_response = supabase.table("registrations").select(
                "*, activities(*)"
            ).eq("id", registration_id).execute()
            
            reg_data = full_response.data[0]
            registration = Registration(**reg_data)
            if reg_data.get("activities"):
                registration.activity = Activity(**reg_data["activities"])
            
            return registration
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update registration"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registration(
    registration_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a registration."""
    supabase = get_supabase_client()
    
    try:
        # Check if registration exists and belongs to user
        existing = supabase.table("registrations").select("id").eq(
            "id", registration_id
        ).eq("user_id", current_user.id).execute()
        
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )
        
        # Delete the registration
        supabase.table("registrations").delete().eq("id", registration_id).execute()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete registration: {str(e)}"
        )