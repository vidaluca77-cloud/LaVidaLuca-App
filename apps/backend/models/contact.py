"""
Contact model for managing contact requests and communications.
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid

from ..database import Base


class Contact(Base):
    """Contact model for contact form submissions and communications."""

    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Contact information
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    organization = Column(String(255))

    # Message details
    subject = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    contact_type = Column(
        String(50), default="general"
    )  # general, partnership, support, etc.

    # Status tracking
    status = Column(String(50), default="new")  # new, in_progress, resolved, closed
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    assigned_to = Column(UUID(as_uuid=True))  # Reference to user handling the request

    # Response tracking
    is_responded = Column(Boolean, default=False)
    response_count = Column(Integer, default=0)
    last_response_at = Column(DateTime(timezone=True))

    # Additional data
    metadata = Column(
        JSON, default=dict
    )  # Flexible additional data like referrer, user agent, etc.
    tags = Column(ARRAY(String), default=list)  # Tags for categorization

    # Privacy and consent
    consent_privacy = Column(Boolean, default=True)
    consent_marketing = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Contact(id={self.id}, name={self.name}, email={self.email}, status={self.status})>"

    def to_dict(self):
        """Convert contact to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "organization": self.organization,
            "subject": self.subject,
            "message": self.message,
            "contact_type": self.contact_type,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": str(self.assigned_to) if self.assigned_to else None,
            "is_responded": self.is_responded,
            "response_count": self.response_count,
            "last_response_at": self.last_response_at.isoformat()
            if self.last_response_at
            else None,
            "metadata": self.metadata or {},
            "tags": self.tags or [],
            "consent_privacy": self.consent_privacy,
            "consent_marketing": self.consent_marketing,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
