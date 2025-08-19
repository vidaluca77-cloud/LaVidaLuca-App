"""
Dependency injection utilities.
"""
from fastapi import Depends, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .config import settings

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


def get_rate_limiter():
    """Get rate limiter instance."""
    return limiter


def rate_limit(calls: int = None, period: str = "1/minute"):
    """Rate limiting decorator."""
    if calls is None:
        calls = settings.rate_limit_per_minute
        period = "1/minute"
    
    return limiter.limit(f"{calls}/{period}")


# Common rate limits
standard_rate_limit = rate_limit()
auth_rate_limit = rate_limit(calls=5, period="1/minute")
upload_rate_limit = rate_limit(calls=10, period="1/minute")


async def verify_content_type(request: Request, allowed_types: list = None):
    """Verify request content type."""
    if allowed_types is None:
        allowed_types = ["application/json"]
    
    content_type = request.headers.get("content-type", "").split(";")[0]
    
    if content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type. Allowed: {', '.join(allowed_types)}"
        )


async def verify_file_size(request: Request):
    """Verify uploaded file size doesn't exceed limit."""
    content_length = request.headers.get("content-length")
    
    if content_length and int(content_length) > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {settings.max_file_size} bytes"
        )