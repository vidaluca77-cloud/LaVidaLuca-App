"""
Session management system.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..models.user import User


class SessionManager:
    """Manages user sessions."""
    
    def __init__(self):
        self.session_expire_hours = 24  # Sessions expire after 24 hours
    
    async def create_session(
        self, 
        db: AsyncSession, 
        user_id: str, 
        user_agent: str = None,
        ip_address: str = None
    ) -> str:
        """
        Create a new user session.
        
        Args:
            db: Database session
            user_id: User ID
            user_agent: User agent string
            ip_address: IP address
            
        Returns:
            Session ID
        """
        session_id = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=self.session_expire_hours)
        
        # Store session data in user profile for now
        # In production, this should be in a separate sessions table or Redis
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            if not user.profile:
                user.profile = {}
            
            if "sessions" not in user.profile:
                user.profile["sessions"] = []
            
            session_data = {
                "session_id": session_id,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": expires_at.isoformat(),
                "user_agent": user_agent,
                "ip_address": ip_address,
                "is_active": True,
                "last_activity": datetime.utcnow().isoformat()
            }
            
            # Remove expired sessions
            user.profile["sessions"] = [
                s for s in user.profile["sessions"]
                if datetime.fromisoformat(s["expires_at"]) > datetime.utcnow()
            ]
            
            # Add new session
            user.profile["sessions"].append(session_data)
            
            # Keep only last 5 sessions
            user.profile["sessions"] = user.profile["sessions"][-5:]
            
            await db.commit()
        
        return session_id
    
    async def get_session(
        self, 
        db: AsyncSession, 
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get session data by session ID.
        
        Args:
            db: Database session
            session_id: Session ID
            
        Returns:
            Session data if found and valid, None otherwise
        """
        # Find user with this session
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        for user in users:
            if user.profile and "sessions" in user.profile:
                for session in user.profile["sessions"]:
                    if (session.get("session_id") == session_id and 
                        session.get("is_active")):
                        
                        # Check if session is expired
                        expires_at = datetime.fromisoformat(session["expires_at"])
                        if datetime.utcnow() < expires_at:
                            # Update last activity
                            session["last_activity"] = datetime.utcnow().isoformat()
                            await db.commit()
                            
                            return {
                                **session,
                                "user_id": str(user.id),
                                "user_email": user.email
                            }
                        else:
                            # Session expired, mark as inactive
                            session["is_active"] = False
                            await db.commit()
        
        return None
    
    async def update_session_activity(
        self, 
        db: AsyncSession, 
        session_id: str
    ) -> bool:
        """
        Update session last activity timestamp.
        
        Args:
            db: Database session
            session_id: Session ID
            
        Returns:
            True if session was found and updated, False otherwise
        """
        session_data = await self.get_session(db, session_id)
        return session_data is not None
    
    async def invalidate_session(
        self, 
        db: AsyncSession, 
        session_id: str
    ) -> bool:
        """
        Invalidate a specific session.
        
        Args:
            db: Database session
            session_id: Session ID to invalidate
            
        Returns:
            True if session was found and invalidated, False otherwise
        """
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        for user in users:
            if user.profile and "sessions" in user.profile:
                for session in user.profile["sessions"]:
                    if session.get("session_id") == session_id:
                        session["is_active"] = False
                        await db.commit()
                        return True
        
        return False
    
    async def invalidate_user_sessions(
        self, 
        db: AsyncSession, 
        user_id: str,
        except_session_id: str = None
    ) -> int:
        """
        Invalidate all sessions for a user.
        
        Args:
            db: Database session
            user_id: User ID
            except_session_id: Session ID to keep active (optional)
            
        Returns:
            Number of sessions invalidated
        """
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user or not user.profile or "sessions" not in user.profile:
            return 0
        
        invalidated = 0
        for session in user.profile["sessions"]:
            if (session.get("is_active") and 
                session.get("session_id") != except_session_id):
                session["is_active"] = False
                invalidated += 1
        
        await db.commit()
        return invalidated
    
    async def get_user_sessions(
        self, 
        db: AsyncSession, 
        user_id: str
    ) -> list[Dict[str, Any]]:
        """
        Get all active sessions for a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of active sessions
        """
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user or not user.profile or "sessions" not in user.profile:
            return []
        
        active_sessions = []
        for session in user.profile["sessions"]:
            if session.get("is_active"):
                expires_at = datetime.fromisoformat(session["expires_at"])
                if datetime.utcnow() < expires_at:
                    active_sessions.append(session)
                else:
                    # Mark expired session as inactive
                    session["is_active"] = False
        
        await db.commit()
        return active_sessions
    
    async def cleanup_expired_sessions(self, db: AsyncSession) -> int:
        """
        Clean up expired sessions from all users.
        
        Args:
            db: Database session
            
        Returns:
            Number of expired sessions cleaned up
        """
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        cleaned_up = 0
        current_time = datetime.utcnow()
        
        for user in users:
            if user.profile and "sessions" in user.profile:
                original_count = len(user.profile["sessions"])
                
                # Remove expired sessions
                user.profile["sessions"] = [
                    s for s in user.profile["sessions"]
                    if datetime.fromisoformat(s["expires_at"]) > current_time
                ]
                
                cleaned_up += original_count - len(user.profile["sessions"])
        
        await db.commit()
        return cleaned_up


# Global instance
session_manager = SessionManager()