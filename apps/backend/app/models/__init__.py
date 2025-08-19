"""
Models package for La Vida Luca application.
"""

from .user import User
from .activity import Activity, ActivitySuggestion

__all__ = ["User", "Activity", "ActivitySuggestion"]