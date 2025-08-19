"""
Audit logging model for security events.
"""

from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from ..database import Base


class AuditLog(Base):
    """Audit log model for tracking security events."""
    
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Event details
    user_id = Column(UUID(as_uuid=True))  # Nullable for system events
    action = Column(String(100), nullable=False, index=True)
    resource = Column(String(100), nullable=False, index=True)
    resource_id = Column(String(100))
    
    # Request context
    ip_address = Column(String(45), index=True)
    user_agent = Column(Text)
    
    # Event outcome
    success = Column(Boolean, nullable=False, index=True)
    error_message = Column(Text)
    
    # Additional details
    details = Column(JSON)  # Flexible storage for event-specific data
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<AuditLog(action={self.action}, resource={self.resource}, success={self.success})>"