"""
User model for authentication and profile management.
"""

from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


class User(Base):
    """User model for authentication and profiles."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile information
    first_name = Column(String(100))
    last_name = Column(String(100))
    profile = Column(JSON, default=dict)  # Flexible profile data
    
    # User status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Security features
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime(timezone=True))
    password_changed_at = Column(DateTime(timezone=True))
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(32))  # TOTP secret
    backup_codes = Column(JSON, default=list)  # 2FA backup codes
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    lockouts = relationship("AccountLockout", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
    
    @property
    def full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
    
    @property
    def is_locked(self):
        """Check if account is currently locked."""
        if self.account_locked_until:
            from datetime import datetime
            return datetime.utcnow() < self.account_locked_until
        return False
    
    def lock_account(self, duration_minutes=30):
        """Lock the account for specified duration."""
        from datetime import datetime, timedelta
        self.account_locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self.failed_login_attempts = 0  # Reset attempts after locking
    
    def unlock_account(self):
        """Unlock the account."""
        self.account_locked_until = None
        self.failed_login_attempts = 0
    
    def increment_failed_attempts(self):
        """Increment failed login attempts."""
        self.failed_login_attempts += 1
        # Auto-lock after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.lock_account(30)  # Lock for 30 minutes
    
    def reset_failed_attempts(self):
        """Reset failed login attempts on successful login."""
        self.failed_login_attempts = 0
    
    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)."""
        return {
            "id": str(self.id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "profile": self.profile,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }