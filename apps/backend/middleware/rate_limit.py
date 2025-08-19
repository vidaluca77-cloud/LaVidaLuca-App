"""
Rate limiting middleware for API endpoints.
"""

from datetime import datetime, timedelta
from typing import Dict, Callable
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
import time

from ..core.security import check_rate_limit, get_rate_limit_reset_time


class RateLimitMiddleware:
    """Rate limiting middleware with configurable limits per endpoint."""
    
    def __init__(self, app):
        self.app = app
        
        # Rate limit configurations per endpoint pattern
        self.rate_limits = {
            # Authentication endpoints - stricter limits
            "/api/v1/auth/login": {"max_requests": 5, "window_minutes": 15},
            "/api/v1/auth/register": {"max_requests": 3, "window_minutes": 60},
            "/api/v1/auth/refresh": {"max_requests": 10, "window_minutes": 15},
            "/api/v1/auth/password-reset": {"max_requests": 3, "window_minutes": 60},
            
            # 2FA endpoints
            "/api/v1/auth/2fa/verify": {"max_requests": 5, "window_minutes": 15},
            "/api/v1/auth/2fa/setup": {"max_requests": 3, "window_minutes": 60},
            
            # General API endpoints - more lenient
            "default": {"max_requests": 100, "window_minutes": 15}
        }
    
    async def __call__(self, request: Request, call_next: Callable):
        """Process request with rate limiting."""
        
        # Skip rate limiting for certain paths
        if self._should_skip_rate_limit(request.url.path):
            return await call_next(request)
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Get rate limit config for this endpoint
        rate_limit_config = self._get_rate_limit_config(request.url.path)
        
        # Create rate limit key
        rate_limit_key = f"rate_limit:{client_ip}:{request.url.path}"
        
        # Check rate limit
        if not check_rate_limit(
            rate_limit_key,
            rate_limit_config["max_requests"],
            rate_limit_config["window_minutes"]
        ):
            # Rate limit exceeded
            reset_time = get_rate_limit_reset_time(
                rate_limit_key, 
                rate_limit_config["window_minutes"]
            )
            
            headers = {
                "X-RateLimit-Limit": str(rate_limit_config["max_requests"]),
                "X-RateLimit-Window": str(rate_limit_config["window_minutes"]),
                "X-RateLimit-Reset": str(int(reset_time.timestamp())) if reset_time else str(int(time.time() + 900))
            }
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Rate limit exceeded. Try again in {rate_limit_config['window_minutes']} minutes.",
                    "error_code": "RATE_LIMIT_EXCEEDED"
                },
                headers=headers
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to response
        response.headers["X-RateLimit-Limit"] = str(rate_limit_config["max_requests"])
        response.headers["X-RateLimit-Window"] = str(rate_limit_config["window_minutes"])
        
        return response
    
    def _should_skip_rate_limit(self, path: str) -> bool:
        """Check if path should skip rate limiting."""
        skip_paths = [
            "/docs",
            "/redoc", 
            "/openapi.json",
            "/health",
            "/metrics"
        ]
        
        return any(path.startswith(skip_path) for skip_path in skip_paths)
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request."""
        # Check for forwarded headers (from load balancers/proxies)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        return request.client.host if request.client else "unknown"
    
    def _get_rate_limit_config(self, path: str) -> Dict[str, int]:
        """Get rate limit configuration for a path."""
        # Check for exact match
        if path in self.rate_limits:
            return self.rate_limits[path]
        
        # Check for pattern matches
        for pattern, config in self.rate_limits.items():
            if pattern != "default" and path.startswith(pattern):
                return config
        
        # Return default configuration
        return self.rate_limits["default"]


def create_rate_limit_response(
    message: str = "Rate limit exceeded", 
    retry_after: int = 900
) -> JSONResponse:
    """Create a standardized rate limit response."""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": message,
            "error_code": "RATE_LIMIT_EXCEEDED",
            "retry_after": retry_after
        },
        headers={
            "Retry-After": str(retry_after)
        }
    )