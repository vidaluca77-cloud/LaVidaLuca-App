"""
Rate limiting information and documentation for OpenAPI.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field


class RateLimitInfo(BaseModel):
    """Rate limiting information."""
    requests_per_window: int = Field(..., description="Number of requests allowed per time window")
    window_seconds: int = Field(..., description="Time window in seconds")
    description: str = Field(..., description="Human-readable description of the rate limit")


class EndpointRateLimits(BaseModel):
    """Rate limits for different endpoint categories."""
    
    # Authentication endpoints
    auth_register: RateLimitInfo = RateLimitInfo(
        requests_per_window=5,
        window_seconds=60,
        description="5 registration attempts per minute per IP address"
    )
    
    auth_login: RateLimitInfo = RateLimitInfo(
        requests_per_window=10,
        window_seconds=60,
        description="10 login attempts per minute per IP address"
    )
    
    auth_verify_token: RateLimitInfo = RateLimitInfo(
        requests_per_window=100,
        window_seconds=60,
        description="100 token verifications per minute per user"
    )
    
    # Activity endpoints
    activities_create: RateLimitInfo = RateLimitInfo(
        requests_per_window=20,
        window_seconds=3600,
        description="20 activity creations per hour per user"
    )
    
    activities_list: RateLimitInfo = RateLimitInfo(
        requests_per_window=100,
        window_seconds=60,
        description="100 activity list requests per minute per IP"
    )
    
    activities_get: RateLimitInfo = RateLimitInfo(
        requests_per_window=200,
        window_seconds=60,
        description="200 activity detail requests per minute per IP"
    )
    
    # User endpoints
    users_profile: RateLimitInfo = RateLimitInfo(
        requests_per_window=100,
        window_seconds=60,
        description="100 profile requests per minute per user"
    )
    
    users_update: RateLimitInfo = RateLimitInfo(
        requests_per_window=10,
        window_seconds=60,
        description="10 profile updates per minute per user"
    )
    
    # Contact endpoints
    contact_create: RateLimitInfo = RateLimitInfo(
        requests_per_window=5,
        window_seconds=60,
        description="5 contact form submissions per minute per IP"
    )
    
    # AI Suggestions endpoints
    suggestions_ai: RateLimitInfo = RateLimitInfo(
        requests_per_window=10,
        window_seconds=3600,
        description="10 AI suggestion requests per hour per user"
    )
    
    suggestions_featured: RateLimitInfo = RateLimitInfo(
        requests_per_window=100,
        window_seconds=60,
        description="100 featured suggestions per minute per IP"
    )
    
    suggestions_similar: RateLimitInfo = RateLimitInfo(
        requests_per_window=50,
        window_seconds=60,
        description="50 similar activity requests per minute per IP"
    )


# Rate limiting documentation for OpenAPI
RATE_LIMIT_DOCUMENTATION = {
    "description": """
## Rate Limiting

This API implements rate limiting to ensure fair usage and protect against abuse. 
Rate limits are applied per IP address for public endpoints and per authenticated user for protected endpoints.

### Rate Limit Headers

All responses include the following headers to inform you about your current rate limit status:

- `X-RateLimit-Limit`: The rate limit ceiling for the given endpoint
- `X-RateLimit-Remaining`: The number of requests left for the time window
- `X-RateLimit-Reset`: The remaining window before the rate limit resets (in UTC epoch seconds)

### Rate Limit Exceeded

When you exceed a rate limit, you'll receive a `429 Too Many Requests` response with details about when you can retry:

```json
{
    "detail": "Rate limit exceeded. Try again in 60 seconds.",
    "retry_after": 60
}
```

### Endpoint-Specific Limits

Different endpoints have different rate limits based on their computational cost and security requirements:

#### Authentication Endpoints
- **Registration**: 5 attempts per minute per IP
- **Login**: 10 attempts per minute per IP  
- **Token Verification**: 100 requests per minute per user

#### Activity Endpoints
- **Create Activity**: 20 creations per hour per user
- **List Activities**: 100 requests per minute per IP
- **Get Activity**: 200 requests per minute per IP

#### User Management
- **Profile Access**: 100 requests per minute per user
- **Profile Updates**: 10 updates per minute per user

#### Contact Forms
- **Submit Contact**: 5 submissions per minute per IP

#### AI Suggestions
- **AI-Powered Suggestions**: 10 requests per hour per user (due to AI processing costs)
- **Featured Suggestions**: 100 requests per minute per IP
- **Similar Activities**: 50 requests per minute per IP

### Best Practices

1. **Cache responses** when possible to reduce API calls
2. **Implement exponential backoff** when you receive rate limit errors
3. **Monitor rate limit headers** to adjust your request frequency
4. **Use pagination** effectively for list endpoints
5. **Batch operations** when available instead of multiple individual requests

### Contact for Higher Limits

If you need higher rate limits for your application, please contact our support team at support@lavidaluca.com with details about your use case.
    """,
    "rate_limits": EndpointRateLimits().dict()
}