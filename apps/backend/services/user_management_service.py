"""
User management service for admin operations.
"""

from typing import Optional, List, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from ..models.user import User
from ..models.session import UserSession, LoginAttempt, AccountLockout
from ..core.security import get_password_hash, PasswordPolicyError
from ..schemas.auth import UserManagement


class UserManagementService:
    """Service for user management and admin operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_users(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_verified: Optional[bool] = None
    ) -> tuple[List[User], int]:
        """Get paginated list of users with optional filtering."""
        query = self.db.query(User)
        
        # Apply filters
        if search:
            search_filter = or_(
                User.email.ilike(f"%{search}%"),
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        if is_verified is not None:
            query = query.filter(User.is_verified == is_verified)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        users = query.order_by(desc(User.created_at)).offset(skip).limit(limit).all()
        
        return users, total
    
    def get_user_details(self, user_id: str) -> Optional[Dict]:
        """Get detailed user information including security stats."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Get user sessions
        active_sessions = self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).count()
        
        # Get recent login attempts
        recent_attempts = self.db.query(LoginAttempt).filter(
            LoginAttempt.email == user.email,
            LoginAttempt.attempted_at >= datetime.utcnow() - timedelta(days=30)
        ).order_by(desc(LoginAttempt.attempted_at)).limit(10).all()
        
        # Get lockout history
        lockouts = self.db.query(AccountLockout).filter(
            AccountLockout.user_id == user_id
        ).order_by(desc(AccountLockout.locked_at)).limit(5).all()
        
        return {
            "user": user,
            "active_sessions": active_sessions,
            "recent_login_attempts": [
                {
                    "ip_address": attempt.ip_address,
                    "success": attempt.success,
                    "attempted_at": attempt.attempted_at,
                    "failure_reason": attempt.failure_reason
                }
                for attempt in recent_attempts
            ],
            "lockout_history": [
                {
                    "locked_at": lockout.locked_at,
                    "locked_until": lockout.locked_until,
                    "reason": lockout.lockout_reason,
                    "failed_attempts": lockout.failed_attempts
                }
                for lockout in lockouts
            ]
        }
    
    def manage_user(
        self, 
        action_data: UserManagement, 
        admin_user_id: str
    ) -> Dict[str, str]:
        """Perform user management action."""
        user = self.db.query(User).filter(User.id == action_data.user_id).first()
        if not user:
            raise ValueError("User not found")
        
        action = action_data.action
        reason = action_data.reason or f"Admin action by {admin_user_id}"
        
        result = {"message": "", "action": action}
        
        if action == "activate":
            if user.is_active:
                result["message"] = "User is already active"
            else:
                user.is_active = True
                result["message"] = "User activated successfully"
        
        elif action == "deactivate":
            if not user.is_active:
                result["message"] = "User is already inactive"
            else:
                user.is_active = False
                # Terminate all sessions
                self._terminate_all_user_sessions(user.id)
                result["message"] = "User deactivated and all sessions terminated"
        
        elif action == "lock":
            if user.is_locked:
                result["message"] = "User is already locked"
            else:
                user.lock_account(duration_minutes=60)  # Lock for 1 hour
                # Create lockout record
                lockout = AccountLockout(
                    user_id=user.id,
                    locked_until=user.account_locked_until,
                    lockout_reason="admin_action",
                    failed_attempts=0
                )
                self.db.add(lockout)
                # Terminate all sessions
                self._terminate_all_user_sessions(user.id)
                result["message"] = "User locked and all sessions terminated"
        
        elif action == "unlock":
            if not user.is_locked:
                result["message"] = "User is not locked"
            else:
                user.unlock_account()
                # Mark latest lockout as resolved
                latest_lockout = self.db.query(AccountLockout).filter(
                    AccountLockout.user_id == user.id,
                    AccountLockout.unlocked_at.is_(None)
                ).order_by(desc(AccountLockout.locked_at)).first()
                if latest_lockout:
                    latest_lockout.unlock()
                result["message"] = "User unlocked successfully"
        
        elif action == "reset_password":
            # Generate a temporary password
            temp_password = self._generate_temp_password()
            user.hashed_password = get_password_hash(temp_password)
            user.password_changed_at = datetime.utcnow()
            # Force password change on next login
            user.profile = user.profile or {}
            user.profile["force_password_change"] = True
            # Terminate all sessions
            self._terminate_all_user_sessions(user.id)
            result["message"] = f"Password reset. Temporary password: {temp_password}"
            result["temp_password"] = temp_password
        
        elif action == "enable_2fa":
            if user.two_factor_enabled:
                result["message"] = "2FA is already enabled"
            else:
                # This would require user interaction to complete
                result["message"] = "2FA setup initiated (requires user verification)"
        
        elif action == "disable_2fa":
            if not user.two_factor_enabled:
                result["message"] = "2FA is not enabled"
            else:
                user.two_factor_enabled = False
                user.two_factor_secret = None
                user.backup_codes = []
                result["message"] = "2FA disabled successfully"
        
        else:
            raise ValueError(f"Unknown action: {action}")
        
        # Log the admin action
        self._log_admin_action(admin_user_id, action, user.id, reason)
        
        self.db.commit()
        return result
    
    def get_security_stats(self) -> Dict:
        """Get security statistics for admin dashboard."""
        now = datetime.utcnow()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)
        last_30d = now - timedelta(days=30)
        
        stats = {}
        
        # User counts
        stats["total_users"] = self.db.query(User).count()
        stats["active_users"] = self.db.query(User).filter(User.is_active == True).count()
        stats["verified_users"] = self.db.query(User).filter(User.is_verified == True).count()
        stats["locked_users"] = self.db.query(User).filter(
            User.account_locked_until > now
        ).count()
        stats["2fa_enabled_users"] = self.db.query(User).filter(
            User.two_factor_enabled == True
        ).count()
        
        # Login attempt stats
        stats["login_attempts_24h"] = self.db.query(LoginAttempt).filter(
            LoginAttempt.attempted_at >= last_24h
        ).count()
        stats["failed_logins_24h"] = self.db.query(LoginAttempt).filter(
            LoginAttempt.attempted_at >= last_24h,
            LoginAttempt.success == False
        ).count()
        
        # Active sessions
        stats["active_sessions"] = self.db.query(UserSession).filter(
            UserSession.is_active == True,
            UserSession.expires_at > now
        ).count()
        
        # Recent lockouts
        stats["lockouts_7d"] = self.db.query(AccountLockout).filter(
            AccountLockout.locked_at >= last_7d
        ).count()
        
        return stats
    
    def get_suspicious_activities(self, limit: int = 50) -> List[Dict]:
        """Get suspicious activities for security monitoring."""
        activities = []
        
        # Multiple failed login attempts
        failed_attempts = self.db.query(LoginAttempt).filter(
            LoginAttempt.success == False,
            LoginAttempt.attempted_at >= datetime.utcnow() - timedelta(hours=24)
        ).order_by(desc(LoginAttempt.attempted_at)).limit(limit).all()
        
        for attempt in failed_attempts:
            activities.append({
                "type": "failed_login",
                "email": attempt.email,
                "ip_address": attempt.ip_address,
                "timestamp": attempt.attempted_at,
                "details": {"reason": attempt.failure_reason}
            })
        
        # Recent lockouts
        lockouts = self.db.query(AccountLockout).filter(
            AccountLockout.locked_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(desc(AccountLockout.locked_at)).limit(limit).all()
        
        for lockout in lockouts:
            user = self.db.query(User).filter(User.id == lockout.user_id).first()
            activities.append({
                "type": "account_lockout",
                "email": user.email if user else "unknown",
                "user_id": str(lockout.user_id),
                "timestamp": lockout.locked_at,
                "details": {
                    "reason": lockout.lockout_reason,
                    "failed_attempts": lockout.failed_attempts
                }
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return activities[:limit]
    
    def _terminate_all_user_sessions(self, user_id: str):
        """Terminate all active sessions for a user."""
        sessions = self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).all()
        
        for session in sessions:
            session.terminate()
            if session.refresh_token:
                session.refresh_token.revoke()
    
    def _generate_temp_password(self) -> str:
        """Generate a temporary password."""
        import secrets
        import string
        
        # Generate 12-character password with mixed case, digits, and symbols
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(12))
        
        # Ensure it meets password policy
        while not self._validate_temp_password(password):
            password = ''.join(secrets.choice(alphabet) for _ in range(12))
        
        return password
    
    def _validate_temp_password(self, password: str) -> bool:
        """Validate temporary password meets policy."""
        import re
        
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        
        return True
    
    def _log_admin_action(self, admin_user_id: str, action: str, target_user_id: str, reason: str):
        """Log admin actions for audit trail."""
        # In a real implementation, this would write to an audit log table
        # For now, we'll just add it to the user's profile for tracking
        pass