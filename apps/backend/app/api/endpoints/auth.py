from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...core.security import (
    verify_password, create_access_token, get_password_hash,
    verify_token, check_rate_limit, RateLimitError, PasswordPolicyError
)
from ...models.user import User
from ...schemas.auth import (
    UserRegister, UserLogin, TokenResponse, RefreshTokenRequest,
    TwoFactorSetup, TwoFactorEnable, TwoFactorVerify,
    SessionList, LogoutRequest
)
from ...schemas.user import UserResponse
from ...core.config import settings
from ...services.session_service import SessionService
from ...services.two_factor_service import TwoFactorService
from ...middleware.rate_limit import create_rate_limit_response


router = APIRouter()
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    token = credentials.credentials
    payload = verify_token(token, "access")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
        )
    
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="User account is locked",
        )
    
    return user


@router.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserRegister, 
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    session_service = SessionService(db)
    
    # Get client info
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    
    # Check rate limiting
    if not session_service.check_login_rate_limit(user_data.email, ip_address):
        return create_rate_limit_response(
            "Too many registration attempts. Please try again later."
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create new user
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
        
    except PasswordPolicyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
def login_user(
    credentials: UserLogin, 
    request: Request,
    db: Session = Depends(get_db)
):
    """Authenticate user and return tokens."""
    session_service = SessionService(db)
    
    # Get client info
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    
    # Check rate limiting
    if not session_service.check_login_rate_limit(credentials.email, ip_address):
        return create_rate_limit_response(
            "Too many login attempts. Please try again later."
        )
    
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        # Record failed attempt
        session_service.record_login_attempt(
            credentials.email, ip_address, user_agent, False, "invalid_credentials"
        )
        
        if user:
            session_service.handle_failed_login(user)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if account is locked
    if user.is_locked:
        session_service.record_login_attempt(
            credentials.email, ip_address, user_agent, False, "account_locked"
        )
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account is temporarily locked due to too many failed attempts"
        )
    
    # Check if account is active
    if not user.is_active:
        session_service.record_login_attempt(
            credentials.email, ip_address, user_agent, False, "account_inactive"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is not active"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires
    )
    
    # Create session and refresh token
    session, refresh_token = session_service.create_session(
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
        device_name=credentials.device_name,
        remember_me=credentials.remember_me
    )
    
    # Record successful login
    session_service.record_login_attempt(
        credentials.email, ip_address, user_agent, True
    )
    session_service.handle_successful_login(user)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        session_id=str(session.id)
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_request: RefreshTokenRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    session_service = SessionService(db)
    
    # Get client info
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    
    # Refresh the token
    user, user_id = session_service.refresh_access_token(
        refresh_request.refresh_token, ip_address, user_agent
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user_id,
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_request.refresh_token,  # Same refresh token
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        session_id=""  # Not creating new session
    )


@router.get("/sessions", response_model=SessionList)
def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all active sessions for the current user."""
    session_service = SessionService(db)
    sessions = session_service.get_user_sessions(str(current_user.id))
    
    return SessionList(
        sessions=[
            {
                "id": str(session.id),
                "device_name": session.device_name,
                "device_fingerprint": session.device_fingerprint,
                "ip_address": session.ip_address,
                "user_agent": session.user_agent,
                "location": session.location,
                "is_current": False,  # Could implement current session detection
                "last_activity": session.last_activity,
                "created_at": session.created_at,
                "expires_at": session.expires_at
            }
            for session in sessions
        ],
        total=len(sessions)
    )


@router.post("/logout")
def logout_user(
    logout_request: LogoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user by terminating sessions."""
    session_service = SessionService(db)
    
    if logout_request.logout_all_devices:
        # Terminate all sessions
        terminated_count = session_service.terminate_all_sessions(str(current_user.id))
        return {"message": f"Logged out from {terminated_count} devices"}
    else:
        # Would need current session ID to terminate just current session
        # For now, terminate all
        terminated_count = session_service.terminate_all_sessions(str(current_user.id))
        return {"message": "Logged out successfully"}


@router.delete("/sessions/{session_id}")
def terminate_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Terminate a specific session."""
    session_service = SessionService(db)
    
    if session_service.terminate_session(session_id, str(current_user.id)):
        return {"message": "Session terminated successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )


# 2FA Endpoints
@router.post("/2fa/setup", response_model=TwoFactorSetup)
def setup_2fa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Setup 2FA for the current user."""
    twofa_service = TwoFactorService(db)
    
    try:
        setup_data = twofa_service.setup_2fa(current_user)
        return TwoFactorSetup(**setup_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/2fa/enable")
def enable_2fa(
    enable_data: TwoFactorEnable,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enable 2FA after verifying the setup token."""
    twofa_service = TwoFactorService(db)
    
    try:
        if twofa_service.enable_2fa(current_user, enable_data.token):
            return {"message": "2FA enabled successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 2FA token"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/2fa/disable")
def disable_2fa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disable 2FA for the current user."""
    twofa_service = TwoFactorService(db)
    
    if twofa_service.disable_2fa(current_user):
        return {"message": "2FA disabled successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA is not enabled"
        )


@router.post("/2fa/verify")
def verify_2fa(
    verify_data: TwoFactorVerify,
    request: Request,
    db: Session = Depends(get_db)
):
    """Verify 2FA token during login (separate endpoint for 2FA flow)."""
    # This would be called after initial login validation
    # Implementation depends on your 2FA flow design
    # For now, return a placeholder
    return {"message": "2FA verification endpoint"}


@router.post("/2fa/backup-codes")
def regenerate_backup_codes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Regenerate backup codes for 2FA."""
    twofa_service = TwoFactorService(db)
    
    try:
        backup_codes = twofa_service.regenerate_backup_codes(current_user)
        return {"backup_codes": backup_codes}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )