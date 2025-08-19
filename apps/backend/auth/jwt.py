"""
Enhanced JWT token handling with refresh token support.
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
import jwt
import secrets
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from ..config import settings
from ..schemas.auth import TokenData


class RefreshToken:
    """Refresh token model for database storage."""
    
    def __init__(self, user_id: str, token: str, expires_at: datetime):
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at
        self.created_at = datetime.utcnow()
        self.is_active = True


class EnhancedJWTHandler:
    """Enhanced JWT handler with refresh token support."""
    
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_hours = settings.JWT_EXPIRATION_HOURS
        self.refresh_token_expire_days = 7  # Refresh tokens last 7 days
        
    def create_access_token(
        self, 
        data: Dict[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=self.access_token_expire_hours)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, user_id: str) -> str:
        """
        Create a refresh token.
        
        Args:
            user_id: User ID to associate with the token
            
        Returns:
            Refresh token string
        """
        # Generate a secure random token
        token = secrets.token_urlsafe(32)
        return token
    
    def create_token_pair(self, user_data: Dict[str, Any]) -> Tuple[str, str]:
        """
        Create both access and refresh tokens.
        
        Args:
            user_data: User data to encode in access token
            
        Returns:
            Tuple of (access_token, refresh_token)
        """
        access_token = self.create_access_token(user_data)
        refresh_token = self.create_refresh_token(user_data["sub"])
        return access_token, refresh_token
    
    def verify_access_token(self, token: str) -> TokenData:
        """
        Verify and decode a JWT access token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Token data
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            exp: int = payload.get("exp")
            token_type: str = payload.get("type")
            
            if user_id is None or email is None or token_type != "access":
                raise credentials_exception
                
            token_data = TokenData(user_id=user_id, email=email, exp=exp)
            return token_data
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise credentials_exception
    
    async def store_refresh_token(
        self, 
        db: AsyncSession, 
        user_id: str, 
        refresh_token: str
    ) -> None:
        """
        Store refresh token in database.
        
        Args:
            db: Database session
            user_id: User ID
            refresh_token: Refresh token to store
        """
        # For now, we'll store in a simple table
        # In production, consider using Redis for better performance
        expires_at = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        # Remove old refresh tokens for this user
        await self.revoke_user_refresh_tokens(db, user_id)
        
        # This would need a proper RefreshToken model in the database
        # For now, we'll add it to the user profile
        from ..models.user import User
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            if not user.profile:
                user.profile = {}
            user.profile["refresh_token"] = refresh_token
            user.profile["refresh_token_expires"] = expires_at.isoformat()
            await db.commit()
    
    async def verify_refresh_token(
        self, 
        db: AsyncSession, 
        refresh_token: str
    ) -> Optional[str]:
        """
        Verify refresh token and return user ID.
        
        Args:
            db: Database session
            refresh_token: Refresh token to verify
            
        Returns:
            User ID if token is valid, None otherwise
        """
        from ..models.user import User
        
        # Find user with this refresh token
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        for user in users:
            if (user.profile and 
                user.profile.get("refresh_token") == refresh_token):
                
                # Check if token is expired
                expires_str = user.profile.get("refresh_token_expires")
                if expires_str:
                    expires_at = datetime.fromisoformat(expires_str)
                    if datetime.utcnow() < expires_at:
                        return str(user.id)
                    else:
                        # Token expired, remove it
                        user.profile.pop("refresh_token", None)
                        user.profile.pop("refresh_token_expires", None)
                        await db.commit()
        
        return None
    
    async def revoke_refresh_token(
        self, 
        db: AsyncSession, 
        refresh_token: str
    ) -> bool:
        """
        Revoke a specific refresh token.
        
        Args:
            db: Database session
            refresh_token: Refresh token to revoke
            
        Returns:
            True if token was found and revoked, False otherwise
        """
        from ..models.user import User
        
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        for user in users:
            if (user.profile and 
                user.profile.get("refresh_token") == refresh_token):
                user.profile.pop("refresh_token", None)
                user.profile.pop("refresh_token_expires", None)
                await db.commit()
                return True
        
        return False
    
    async def revoke_user_refresh_tokens(
        self, 
        db: AsyncSession, 
        user_id: str
    ) -> None:
        """
        Revoke all refresh tokens for a user.
        
        Args:
            db: Database session
            user_id: User ID
        """
        from ..models.user import User
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user and user.profile:
            user.profile.pop("refresh_token", None)
            user.profile.pop("refresh_token_expires", None)
            await db.commit()


# Global instance
jwt_handler = EnhancedJWTHandler()