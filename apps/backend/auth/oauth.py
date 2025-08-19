"""
OAuth integration for social login providers.
"""

import secrets
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import httpx
from urllib.parse import urlencode

from ..config import settings


class OAuthProvider:
    """Base OAuth provider class."""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
    
    def get_authorization_url(self, state: str = None) -> str:
        """Get authorization URL for OAuth flow."""
        raise NotImplementedError
    
    async def get_access_token(self, code: str, state: str = None) -> str:
        """Exchange authorization code for access token."""
        raise NotImplementedError
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information using access token."""
        raise NotImplementedError


class GoogleOAuthProvider(OAuthProvider):
    """Google OAuth2 provider."""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        super().__init__(client_id, client_secret, redirect_uri)
        self.auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        self.scope = "openid email profile"
    
    def get_authorization_url(self, state: str = None) -> str:
        """Get Google authorization URL."""
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "response_type": "code",
            "access_type": "offline",
            "state": state,
        }
        
        return f"{self.auth_url}?{urlencode(params)}"
    
    async def get_access_token(self, code: str, state: str = None) -> str:
        """Exchange Google authorization code for access token."""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, data=data)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get access token from Google"
                )
            
            token_data = response.json()
            return token_data.get("access_token")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get Google user information."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.user_info_url, headers=headers)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get user info from Google"
                )
            
            user_data = response.json()
            
            return {
                "provider": "google",
                "provider_id": user_data.get("id"),
                "email": user_data.get("email"),
                "first_name": user_data.get("given_name"),
                "last_name": user_data.get("family_name"),
                "picture": user_data.get("picture"),
                "verified": user_data.get("verified_email", False),
            }


class GitHubOAuthProvider(OAuthProvider):
    """GitHub OAuth provider."""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        super().__init__(client_id, client_secret, redirect_uri)
        self.auth_url = "https://github.com/login/oauth/authorize"
        self.token_url = "https://github.com/login/oauth/access_token"
        self.user_info_url = "https://api.github.com/user"
        self.user_email_url = "https://api.github.com/user/emails"
        self.scope = "user:email"
    
    def get_authorization_url(self, state: str = None) -> str:
        """Get GitHub authorization URL."""
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": state,
        }
        
        return f"{self.auth_url}?{urlencode(params)}"
    
    async def get_access_token(self, code: str, state: str = None) -> str:
        """Exchange GitHub authorization code for access token."""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }
        
        headers = {"Accept": "application/json"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, data=data, headers=headers)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get access token from GitHub"
                )
            
            token_data = response.json()
            return token_data.get("access_token")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get GitHub user information."""
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with httpx.AsyncClient() as client:
            # Get user profile
            user_response = await client.get(self.user_info_url, headers=headers)
            
            if user_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get user info from GitHub"
                )
            
            user_data = user_response.json()
            
            # Get user emails
            email_response = await client.get(self.user_email_url, headers=headers)
            email_data = email_response.json() if email_response.status_code == 200 else []
            
            # Find primary email
            primary_email = None
            for email in email_data:
                if email.get("primary", False):
                    primary_email = email.get("email")
                    break
            
            # Fallback to first email or user email from profile
            if not primary_email and email_data:
                primary_email = email_data[0].get("email")
            if not primary_email:
                primary_email = user_data.get("email")
            
            return {
                "provider": "github",
                "provider_id": str(user_data.get("id")),
                "email": primary_email,
                "first_name": user_data.get("name", "").split(" ")[0] if user_data.get("name") else None,
                "last_name": " ".join(user_data.get("name", "").split(" ")[1:]) if user_data.get("name") and len(user_data.get("name", "").split(" ")) > 1 else None,
                "picture": user_data.get("avatar_url"),
                "verified": True,  # GitHub emails are considered verified
                "username": user_data.get("login"),
            }


class OAuthManager:
    """Manages OAuth providers and flow."""
    
    def __init__(self):
        self.providers: Dict[str, OAuthProvider] = {}
        self._setup_providers()
        
        # Store OAuth states temporarily (in production, use Redis)
        self._oauth_states: Dict[str, Dict[str, Any]] = {}
    
    def _setup_providers(self):
        """Setup OAuth providers based on configuration."""
        # Google OAuth
        google_client_id = getattr(settings, "GOOGLE_OAUTH_CLIENT_ID", None)
        google_client_secret = getattr(settings, "GOOGLE_OAUTH_CLIENT_SECRET", None)
        
        if google_client_id and google_client_secret:
            self.providers["google"] = GoogleOAuthProvider(
                client_id=google_client_id,
                client_secret=google_client_secret,
                redirect_uri=f"{settings.CORS_ORIGINS[0]}/api/v1/auth/oauth/google/callback"
            )
        
        # GitHub OAuth
        github_client_id = getattr(settings, "GITHUB_OAUTH_CLIENT_ID", None)
        github_client_secret = getattr(settings, "GITHUB_OAUTH_CLIENT_SECRET", None)
        
        if github_client_id and github_client_secret:
            self.providers["github"] = GitHubOAuthProvider(
                client_id=github_client_id,
                client_secret=github_client_secret,
                redirect_uri=f"{settings.CORS_ORIGINS[0]}/api/v1/auth/oauth/github/callback"
            )
    
    def get_provider(self, provider_name: str) -> Optional[OAuthProvider]:
        """Get OAuth provider by name."""
        return self.providers.get(provider_name)
    
    def get_available_providers(self) -> list[str]:
        """Get list of available OAuth providers."""
        return list(self.providers.keys())
    
    def create_oauth_state(self, provider: str, redirect_url: str = None) -> str:
        """Create OAuth state for CSRF protection."""
        state = secrets.token_urlsafe(32)
        self._oauth_states[state] = {
            "provider": provider,
            "redirect_url": redirect_url,
            "created_at": __import__("time").time()
        }
        return state
    
    def verify_oauth_state(self, state: str, provider: str) -> Optional[Dict[str, Any]]:
        """Verify OAuth state and return state data."""
        state_data = self._oauth_states.get(state)
        
        if not state_data:
            return None
        
        # Check if state is for correct provider
        if state_data.get("provider") != provider:
            return None
        
        # Check if state is not too old (5 minutes)
        if __import__("time").time() - state_data.get("created_at", 0) > 300:
            self._oauth_states.pop(state, None)
            return None
        
        # Remove used state
        self._oauth_states.pop(state, None)
        return state_data
    
    def cleanup_old_states(self):
        """Cleanup old OAuth states."""
        current_time = __import__("time").time()
        expired_states = [
            state for state, data in self._oauth_states.items()
            if current_time - data.get("created_at", 0) > 300
        ]
        
        for state in expired_states:
            self._oauth_states.pop(state, None)


# Global instance
oauth_manager = OAuthManager()