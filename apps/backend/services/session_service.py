"""
Session management service for handling user sessions and refresh tokens.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
import secrets

from ..models.user import User
from ..models.session import RefreshToken, UserSession, LoginAttempt, AccountLockout
from ..core.security import (
    create_refresh_token, 
    verify_refresh_token_hash,
    generate_device_fingerprint,
    check_rate_limit,
    RateLimitError
)
from ..core.config import settings


class SessionService:
    """Service for managing user sessions and refresh tokens."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_session(
        self, 
        user: User, 
        ip_address: str, 
        user_agent: str,
        device_name: Optional[str] = None,
        remember_me: bool = False
    ) -> tuple[UserSession, str]:
        """Create a new user session with refresh token."""
        
        # Generate device fingerprint
        device_fingerprint = generate_device_fingerprint(user_agent, ip_address)
        
        # Create refresh token
        refresh_token, token_hash = create_refresh_token(str(user.id))
        
        # Set expiration based on remember_me flag
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        if remember_me:
            expires_delta = timedelta(days=90)  # 3 months for remember me
        
        # Create refresh token record
        refresh_token_record = RefreshToken(
            token_hash=token_hash,
            user_id=user.id,
            expires_at=datetime.utcnow() + expires_delta,
            device_fingerprint=device_fingerprint,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.db.add(refresh_token_record)
        self.db.flush()  # Get the ID
        
        # Create session record
        session = UserSession(
            user_id=user.id,
            refresh_token_id=refresh_token_record.id,
            session_token=secrets.token_urlsafe(32),
            device_name=device_name or self._extract_device_name(user_agent),
            device_fingerprint=device_fingerprint,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.utcnow() + expires_delta
        )
        
        self.db.add(session)
        self.db.commit()
        
        return session, refresh_token
    
    def refresh_access_token(
        self, 
        refresh_token: str, 
        ip_address: str, 
        user_agent: str
    ) -> tuple[Optional[User], Optional[str]]:
        """Refresh access token using refresh token."""
        
        # Find refresh token record
        refresh_token_record = self.db.query(RefreshToken).filter(
            RefreshToken.is_revoked == False
        ).all()
        
        valid_token = None
        for record in refresh_token_record:
            if verify_refresh_token_hash(refresh_token, record.token_hash):
                valid_token = record
                break
        
        if not valid_token or not valid_token.is_valid:
            return None, None
        
        # Verify device fingerprint for security
        current_fingerprint = generate_device_fingerprint(user_agent, ip_address)
        if current_fingerprint != valid_token.device_fingerprint:
            # Revoke token due to suspicious activity
            valid_token.revoke()
            self.db.commit()
            return None, None
        
        # Update last used time
        valid_token.used_at = datetime.utcnow()
        
        # Get user
        user = self.db.query(User).filter(User.id == valid_token.user_id).first()
        if not user or not user.is_active or user.is_locked:
            return None, None
        
        # Update session activity
        session = self.db.query(UserSession).filter(
            UserSession.refresh_token_id == valid_token.id,
            UserSession.is_active == True
        ).first()
        
        if session:
            session.update_activity()
        
        self.db.commit()
        
        return user, str(user.id)
    
    def get_user_sessions(self, user_id: str) -> List[UserSession]:
        """Get all active sessions for a user."""
        return self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).order_by(UserSession.last_activity.desc()).all()
    
    def terminate_session(self, session_id: str, user_id: str) -> bool:
        """Terminate a specific session."""
        session = self.db.query(UserSession).filter(
            UserSession.id == session_id,
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).first()
        
        if not session:
            return False
        
        session.terminate()
        
        # Revoke associated refresh token
        if session.refresh_token:
            session.refresh_token.revoke()
        
        self.db.commit()
        return True
    
    def terminate_all_sessions(self, user_id: str, except_session_id: Optional[str] = None) -> int:
        """Terminate all sessions for a user except optionally one."""
        query = self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        )
        
        if except_session_id:
            query = query.filter(UserSession.id != except_session_id)
        
        sessions = query.all()
        
        for session in sessions:
            session.terminate()
            if session.refresh_token:
                session.refresh_token.revoke()
        
        self.db.commit()
        return len(sessions)
    
    def record_login_attempt(
        self, 
        email: str, 
        ip_address: str, 
        user_agent: str, 
        success: bool,
        failure_reason: Optional[str] = None
    ):
        """Record a login attempt for security monitoring."""
        attempt = LoginAttempt(
            email=email,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            failure_reason=failure_reason
        )
        
        self.db.add(attempt)
        self.db.commit()
    
    def check_login_rate_limit(self, email: str, ip_address: str) -> bool:
        """Check if login attempts are rate limited."""
        # Check by email
        email_key = f"login_email:{email}"
        if not check_rate_limit(
            email_key, 
            settings.LOGIN_RATE_LIMIT_ATTEMPTS, 
            settings.LOGIN_RATE_LIMIT_WINDOW
        ):
            return False
        
        # Check by IP
        ip_key = f"login_ip:{ip_address}"
        if not check_rate_limit(
            ip_key, 
            settings.LOGIN_RATE_LIMIT_ATTEMPTS * 3,  # More lenient for IP
            settings.LOGIN_RATE_LIMIT_WINDOW
        ):
            return False
        
        return True
    
    def handle_failed_login(self, user: User):
        """Handle failed login attempt - increment counter and potentially lock account."""
        user.increment_failed_attempts()
        
        if user.failed_login_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
            # Create lockout record
            lockout = AccountLockout(
                user_id=user.id,
                locked_until=datetime.utcnow() + timedelta(minutes=settings.ACCOUNT_LOCKOUT_DURATION),
                failed_attempts=user.failed_login_attempts,
                lockout_reason="too_many_failed_attempts"
            )
            self.db.add(lockout)
        
        self.db.commit()
    
    def handle_successful_login(self, user: User):
        """Handle successful login - reset failed attempts and update last login."""
        user.reset_failed_attempts()
        user.last_login = datetime.utcnow()
        self.db.commit()
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions and refresh tokens."""
        now = datetime.utcnow()
        
        # Terminate expired sessions
        expired_sessions = self.db.query(UserSession).filter(
            UserSession.expires_at < now,
            UserSession.is_active == True
        ).all()
        
        for session in expired_sessions:
            session.terminate()
        
        # Revoke expired refresh tokens
        expired_tokens = self.db.query(RefreshToken).filter(
            RefreshToken.expires_at < now,
            RefreshToken.is_revoked == False
        ).all()
        
        for token in expired_tokens:
            token.revoke()
        
        self.db.commit()
        
        return len(expired_sessions), len(expired_tokens)
    
    @staticmethod
    def _extract_device_name(user_agent: str) -> str:
        """Extract a friendly device name from user agent."""
        if not user_agent:
            return "Unknown Device"
        
        user_agent = user_agent.lower()
        
        if 'mobile' in user_agent or 'android' in user_agent:
            if 'chrome' in user_agent:
                return "Mobile Chrome"
            elif 'firefox' in user_agent:
                return "Mobile Firefox"
            elif 'safari' in user_agent:
                return "Mobile Safari"
            else:
                return "Mobile Browser"
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            return "Tablet"
        elif 'windows' in user_agent:
            if 'chrome' in user_agent:
                return "Windows Chrome"
            elif 'firefox' in user_agent:
                return "Windows Firefox"
            elif 'edge' in user_agent:
                return "Windows Edge"
            else:
                return "Windows Browser"
        elif 'mac' in user_agent:
            if 'chrome' in user_agent:
                return "Mac Chrome"
            elif 'firefox' in user_agent:
                return "Mac Firefox"
            elif 'safari' in user_agent:
                return "Mac Safari"
            else:
                return "Mac Browser"
        elif 'linux' in user_agent:
            return "Linux Browser"
        else:
            return "Unknown Browser"