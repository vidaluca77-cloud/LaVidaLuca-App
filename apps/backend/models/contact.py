"""
Contact model for managing contact requests and communications.
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, Integer, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .base import Base, BaseEntityMixin


class Contact(Base, BaseEntityMixin):
    """Contact model for contact form submissions and communications."""
    
    __tablename__ = "contacts"
    
    # Contact information
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50))
    organization = Column(String(255))
    
    # Message details
    subject = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    contact_type = Column(String(50), default="general", index=True)  # general, partnership, support, etc.
    
    # Status tracking
    status = Column(String(50), default="new", index=True)  # new, in_progress, resolved, closed
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    assigned_to = Column(UUID(as_uuid=True), ForeignKey('users.id'))  # Reference to user handling the request
    
    # Response tracking
    is_responded = Column(Boolean, default=False, index=True)
    response_count = Column(Integer, default=0)
    last_response_at = Column(DateTime(timezone=True))
    
    # Additional data
    metadata = Column(JSON, default=dict)  # Flexible additional data like referrer, user agent, etc.
    tags = Column(ARRAY(String), default=list)  # Tags for categorization
    
    # Privacy and consent
    consent_privacy = Column(Boolean, default=True)
    consent_marketing = Column(Boolean, default=False)
    
    # Relationships
    assigned_user = relationship("User", back_populates="assigned_contacts")
    
    def __repr__(self):
        return f"<Contact(id={self.id}, name={self.name}, email={self.email}, status={self.status})>"
    
    def to_dict(self):
        """Convert contact to dictionary."""
        data = super().to_dict()
        if data.get('assigned_to'):
            data['assigned_to'] = str(data['assigned_to'])
        return data


# Create indexes for search optimization
Index('ix_contacts_email_type', Contact.email, Contact.contact_type)
Index('ix_contacts_status_priority', Contact.status, Contact.priority)
Index('ix_contacts_assigned_status', Contact.assigned_to, Contact.status)
Index('ix_contacts_created_status', Contact.created_at, Contact.status)
Index('ix_contacts_response_tracking', Contact.is_responded, Contact.last_response_at)