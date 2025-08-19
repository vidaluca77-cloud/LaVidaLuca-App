"""
Comprehensive error response schemas for OpenAPI documentation.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Individual error detail."""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    field: Optional[str] = Field(None, description="Field that caused the error (for validation errors)")


class ValidationErrorDetail(BaseModel):
    """Validation error detail from Pydantic."""
    loc: List[str] = Field(..., description="Location of the error in the request")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")


class ErrorResponse(BaseModel):
    """Standard error response format."""
    detail: str = Field(..., description="Error message")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "General error",
                    "value": {
                        "detail": "An error occurred"
                    }
                }
            ]
        }


class ValidationErrorResponse(BaseModel):
    """Validation error response format."""
    detail: List[ValidationErrorDetail] = Field(..., description="List of validation errors")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "Validation error",
                    "value": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            },
                            {
                                "loc": ["body", "password"],
                                "msg": "ensure this value has at least 8 characters",
                                "type": "value_error.any_str.min_length"
                            }
                        ]
                    }
                }
            ]
        }


class NotFoundErrorResponse(BaseModel):
    """Not found error response."""
    detail: str = Field(default="Not found", description="Resource not found message")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "Resource not found",
                    "value": {
                        "detail": "User not found"
                    }
                },
                {
                    "summary": "Activity not found", 
                    "value": {
                        "detail": "Activity not found"
                    }
                }
            ]
        }


class UnauthorizedErrorResponse(BaseModel):
    """Unauthorized error response."""
    detail: str = Field(default="Not authenticated", description="Authentication error message")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "Not authenticated",
                    "value": {
                        "detail": "Not authenticated"
                    }
                },
                {
                    "summary": "Invalid credentials",
                    "value": {
                        "detail": "Incorrect email or password"
                    }
                },
                {
                    "summary": "Invalid token",
                    "value": {
                        "detail": "Could not validate credentials"
                    }
                }
            ]
        }


class ForbiddenErrorResponse(BaseModel):
    """Forbidden error response."""
    detail: str = Field(default="Not enough permissions", description="Permission error message")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "Insufficient permissions",
                    "value": {
                        "detail": "Not enough permissions"
                    }
                },
                {
                    "summary": "Admin required",
                    "value": {
                        "detail": "Administrator privileges required"
                    }
                }
            ]
        }


class ConflictErrorResponse(BaseModel):
    """Conflict error response."""
    detail: str = Field(default="Resource already exists", description="Conflict error message")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "Email already registered",
                    "value": {
                        "detail": "Email already registered"
                    }
                },
                {
                    "summary": "Username taken",
                    "value": {
                        "detail": "Username already exists"
                    }
                }
            ]
        }


class RateLimitErrorResponse(BaseModel):
    """Rate limit error response."""
    detail: str = Field(default="Rate limit exceeded", description="Rate limit error message")
    retry_after: Optional[int] = Field(None, description="Seconds to wait before retrying")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "Rate limit exceeded",
                    "value": {
                        "detail": "Rate limit exceeded. Try again in 60 seconds.",
                        "retry_after": 60
                    }
                }
            ]
        }


class ServiceUnavailableErrorResponse(BaseModel):
    """Service unavailable error response."""
    detail: str = Field(default="Service temporarily unavailable", description="Service error message")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "AI service unavailable",
                    "value": {
                        "detail": "AI suggestions service is not available"
                    }
                },
                {
                    "summary": "Database unavailable",
                    "value": {
                        "detail": "Database service is temporarily unavailable"
                    }
                }
            ]
        }


class InternalServerErrorResponse(BaseModel):
    """Internal server error response."""
    detail: str = Field(default="Internal server error", description="Server error message")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "Server error",
                    "value": {
                        "detail": "An internal error occurred. Please try again later."
                    }
                }
            ]
        }


# Common error responses dictionary for reuse in route decorators
COMMON_ERROR_RESPONSES = {
    400: {
        "model": ErrorResponse,
        "description": "Bad Request"
    },
    401: {
        "model": UnauthorizedErrorResponse,
        "description": "Unauthorized"
    },
    403: {
        "model": ForbiddenErrorResponse,
        "description": "Forbidden"
    },
    404: {
        "model": NotFoundErrorResponse,
        "description": "Not Found"
    },
    409: {
        "model": ConflictErrorResponse,
        "description": "Conflict"
    },
    422: {
        "model": ValidationErrorResponse,
        "description": "Validation Error"
    },
    429: {
        "model": RateLimitErrorResponse,
        "description": "Too Many Requests"
    },
    500: {
        "model": InternalServerErrorResponse,
        "description": "Internal Server Error"
    },
    503: {
        "model": ServiceUnavailableErrorResponse,
        "description": "Service Unavailable"
    }
}