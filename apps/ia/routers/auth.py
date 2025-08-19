from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models import User
from schemas import LoginRequest, Token
from auth import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: LoginRequest, db: Session = Depends(get_db)):
    """Connexion utilisateur et génération du token JWT"""
    user = db.query(User).filter(User.email == form_data.email).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(hours=24)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}