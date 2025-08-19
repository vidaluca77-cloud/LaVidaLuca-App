"""
Schemas package for La Vida Luca application.
"""

from .user import (
    User, UserCreate, UserUpdate, UserProfile, UserLogin, 
    UserRegistration, UserChangePassword
)
from .activity import (
    Activity, ActivityCreate, ActivityUpdate, ActivitySummary,
    ActivitySuggestion, ActivitySuggestionCreate, ActivitySearchFilters
)
from .auth import (
    Token, TokenData, RefreshToken, PasswordReset, PasswordResetConfirm
)

__all__ = [
    # User schemas
    "User", "UserCreate", "UserUpdate", "UserProfile", "UserLogin", 
    "UserRegistration", "UserChangePassword",
    # Activity schemas
    "Activity", "ActivityCreate", "ActivityUpdate", "ActivitySummary",
    "ActivitySuggestion", "ActivitySuggestionCreate", "ActivitySearchFilters",
    # Auth schemas
    "Token", "TokenData", "RefreshToken", "PasswordReset", "PasswordResetConfirm"
]