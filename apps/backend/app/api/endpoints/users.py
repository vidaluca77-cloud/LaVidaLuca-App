from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...api.deps import get_current_active_user
from ...models.models import User
from ...schemas.schemas import User as UserSchema


router = APIRouter()


@router.get("/me", response_model=UserSchema)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/", response_model=List[UserSchema])
def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Only superusers can list all users
    if not current_user.is_superuser:
        return [current_user]
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users