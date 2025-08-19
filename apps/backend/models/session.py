"""
Session and refresh token models for enhanced authentication.
"""

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timedelta

from ..database import Base


class RefreshToken(Base):
    """Refresh token model for JWT token rotation."""
    
    __tablename__ = "refresh_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Token metadata
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    device_fingerprint = Column(String(255))  # Browser/device identification
    ip_address = Column(String(45))  # IPv4/IPv6 address
    user_agent = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    used_at = Column(DateTime(timezone=True))  # When token was last used
    revoked_at = Column(DateTime(timezone=True))
    
    # Relationship
    user = relationship("User", back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>"
    
    @property
    def is_expired(self):
        """Check if refresh token is expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self):
        """Check if refresh token is valid (not expired or revoked)."""
        return not self.is_expired and not self.is_revoked
    
    def revoke(self):
        """Revoke the refresh token."""
        self.is_revoked = True
        self.revoked_at = datetime.utcnow()


class UserSession(Base):
    """User session model for tracking active sessions across devices."""
    
    __tablename__ = "user_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    refresh_token_id = Column(UUID(as_uuid=True), ForeignKey("refresh_tokens.id"), nullable=False)
    
    # Session metadata
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    device_name = Column(String(255))  # User-friendly device name
    device_fingerprint = Column(String(255), nullable=False)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(Text)
    location = Column(String(255))  # Geographic location (optional)
    
    # Session status
    is_active = Column(Boolean, default=True)
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    terminated_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    refresh_token = relationship("RefreshToken")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, device_name={self.device_name})>"
    
    @property
    def is_expired(self):
        """Check if session is expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self):
        """Check if session is valid (active and not expired)."""
        return self.is_active and not self.is_expired
    
    def terminate(self):
        """Terminate the session."""
        self.is_active = False
        self.terminated_at = datetime.utcnow()
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()


class LoginAttempt(Base):
    """Track login attempts for rate limiting and security monitoring."""
    
    __tablename__ = "login_attempts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, index=True)
    ip_address = Column(String(45), nullable=False, index=True)
    user_agent = Column(Text)
    
    # Attempt details
    success = Column(Boolean, nullable=False)
    failure_reason = Column(String(100))  # 'invalid_credentials', 'account_locked', etc.
    
    # Timestamps
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<LoginAttempt(email={self.email}, success={self.success}, attempted_at={self.attempted_at})>"


class AccountLockout(Base):
    """Track account lockouts for security."""
    
    __tablename__ = "account_lockouts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Lockout details
    locked_until = Column(DateTime(timezone=True), nullable=False)
    failed_attempts = Column(Integer, default=0)
    lockout_reason = Column(String(100))  # 'too_many_failed_attempts', 'security_breach', etc.
    
    # Timestamps
    locked_at = Column(DateTime(timezone=True), server_default=func.now())
    unlocked_at = Column(DateTime(timezone=True))
    
    # Relationship
    user = relationship("User", back_populates="lockouts")
    
    def __repr__(self):
        return f"<AccountLockout(user_id={self.user_id}, locked_until={self.locked_until})>"
    
    @property
    def is_active(self):
        """Check if lockout is still active."""
        return datetime.utcnow() < self.locked_until and self.unlocked_at is None
    
    def unlock(self):
        """Unlock the account."""
        self.unlocked_at = datetime.utcnow()