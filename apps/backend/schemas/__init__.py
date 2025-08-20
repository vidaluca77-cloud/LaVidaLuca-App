"""
Pydantic schemas for request/response validation.
"""

from .auth import *
from .user import *
from .activity import *
from .contact import *
from .consultation import *
from .common import *

__all__ = [
    # Auth schemas
    "UserLogin",
    "UserRegister",
    "Token",
    "TokenData",
    
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserProfile",
    
    # Activity schemas
    "ActivityBase",
    "ActivityCreate",
    "ActivityUpdate",
    "ActivityResponse",
    "ActivitySearchFilters",
    
    # Contact schemas
    "ContactBase",
    "ContactCreate",
    "ContactUpdate",
    "ContactResponse",
    
    # Consultation schemas
    "ConsultationCreate",
    "ConsultationResponse",
    "ConsultationList",
    "ConsultationQuery",
    "AIAssistantRequest",
    "AIAssistantResponse",
    
    # Common schemas
    "ApiResponse",
    "ErrorResponse",
    "PaginationParams",
    "PaginatedResponse",
]