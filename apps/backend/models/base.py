"""
Base models and mixins for SQLAlchemy models.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class TimestampMixin:
    """Mixin for adding timestamp fields to models."""
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class UUIDMixin:
    """Mixin for adding UUID primary key to models."""
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)


class BaseModelMixin:
    """Base model mixin with common functionality."""
    
    def to_dict(self, exclude_fields=None):
        """
        Convert model instance to dictionary.
        
        Args:
            exclude_fields: List of field names to exclude from the result
        """
        if exclude_fields is None:
            exclude_fields = []
            
        result = {}
        for column in self.__table__.columns:
            if column.name not in exclude_fields:
                value = getattr(self, column.name)
                if isinstance(value, datetime):
                    value = value.isoformat()
                elif isinstance(value, uuid.UUID):
                    value = str(value)
                result[column.name] = value
        return result
    
    def update_from_dict(self, data):
        """Update model instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self):
        """String representation of the model."""
        if hasattr(self, 'id'):
            return f"<{self.__class__.__name__}(id={self.id})>"
        return f"<{self.__class__.__name__}()>"


# Create the declarative base
Base = declarative_base()


# Combined mixin for common use cases
class BaseEntityMixin(UUIDMixin, TimestampMixin, BaseModelMixin):
    """Combined mixin with UUID, timestamp fields and common methods."""
    pass