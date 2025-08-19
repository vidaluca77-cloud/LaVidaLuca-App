"""
Database models.
"""
# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .activity import Activity
from .recommendation import Recommendation

__all__ = ["User", "Activity", "Recommendation"]