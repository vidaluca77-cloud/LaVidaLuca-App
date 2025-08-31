from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...core.security import verify_password, create_access_token, get_password_hash
from ...models.models import User
from ...schemas.schemas import UserCreate, User as UserSchema, Token, UserLogin
from ...core.config import settings


router = APIRouter()


@router.post("/register", response_model=UserSchema, summary="Register a new user")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    Creates a new user with the provided information. The username and email must be unique.
    Password will be hashed before storage.

    - **email**: Valid email address (must be unique)
    - **username**: Unique username (3-50 characters)
    - **full_name**: Optional full name for display
    - **password**: Password (minimum 8 characters)
    - **is_active**: Whether the account is active (default: true)

    Returns the created user information (without password).
    """
    # Check if user already exists
    db_user = (
        db.query(User)
        .filter((User.email == user.email) | (User.username == user.username))
        .first()
    )
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email or username already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=user.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token, summary="Login user")
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT access token.

    Validates user credentials and returns a JWT token that can be used
    for authentication in subsequent API calls.

    - **username**: The username for the account
    - **password**: The password for the account

    Returns:
    - **access_token**: JWT token for API authentication
    - **token_type**: Always "bearer"

    The token should be included in the Authorization header as:
    `Authorization: Bearer <access_token>`
    """
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
