from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.crud.crud import get_application, get_applications, create_application, update_application
from app.schemas.schemas import Application, ApplicationCreate, ApplicationUpdate
from app.models.models import User as UserModel

router = APIRouter()

@router.get("/", response_model=List[Application])
def read_applications(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    # Regular users can only see their own applications
    if not current_user.is_superuser:
        user_id = current_user.id
    
    applications = get_applications(db, skip=skip, limit=limit, user_id=user_id)
    return applications

@router.get("/me", response_model=List[Application])
def read_my_applications(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    applications = get_applications(db, skip=skip, limit=limit, user_id=current_user.id)
    return applications

@router.get("/{application_id}", response_model=Application)
def read_application(
    application_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    db_application = get_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Users can only see their own applications unless they're superuser
    if db_application.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return db_application

@router.post("/", response_model=Application)
def create_application_endpoint(
    application: ApplicationCreate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    db_application = create_application(db=db, application=application, user_id=current_user.id)
    return db_application

@router.put("/{application_id}", response_model=Application)
def update_application_endpoint(
    application_id: int, 
    application_update: ApplicationUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    db_application = get_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Users can only update their own applications, superusers can update any
    if db_application.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Regular users can only update message, superusers can update status
    if not current_user.is_superuser and "status" in application_update.model_dump(exclude_unset=True):
        raise HTTPException(status_code=403, detail="Not authorized to update status")
    
    updated_application = update_application(db, application_id=application_id, application_update=application_update)
    return updated_application