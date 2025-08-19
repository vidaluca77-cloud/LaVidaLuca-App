"""
Rate limiting middleware to prevent abuse.
"""

import time
from collections import defaultdict, deque
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Dict, Deque, Tuple
import asyncio


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using sliding window algorithm.
    """
    
    def __init__(
        self, 
        app, 
        requests_per_minute: int = 100,
        requests_per_minute_anonymous: int = 20,
        burst_size: int = 10
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_minute_anonymous = requests_per_minute_anonymous
        self.burst_size = burst_size
        
        # Store request timestamps for each IP
        self._request_times: Dict[str, Deque[float]] = defaultdict(lambda: deque())
        
        # Store burst counts for each IP
        self._burst_counts: Dict[str, int] = defaultdict(int)
        self._burst_reset_times: Dict[str, float] = defaultdict(float)
        
        # Lock for thread safety
        self._lock = asyncio.Lock()
    
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Process request with rate limiting.
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Check rate limits
        if not await self._check_rate_limit(client_ip, request):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self._get_limit_for_request(request)),
                    "X-RateLimit-Remaining": "0"
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = await self._get_remaining_requests(client_ip, request)
        response.headers["X-RateLimit-Limit"] = str(self._get_limit_for_request(request))
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Get client IP address from request.
        """
        # Check for forwarded headers (when behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to client host
        if hasattr(request.client, "host"):
            return request.client.host
        
        return "unknown"
    
    def _get_limit_for_request(self, request: Request) -> int:
        """
        Get rate limit for this request based on authentication status.
        """
        # Check if user is authenticated
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return self.requests_per_minute
        else:
            return self.requests_per_minute_anonymous
    
    async def _check_rate_limit(self, client_ip: str, request: Request) -> bool:
        """
        Check if request is within rate limits.
        """
        async with self._lock:
            current_time = time.time()
            limit = self._get_limit_for_request(request)
            
            # Clean old entries (older than 1 minute)
            request_times = self._request_times[client_ip]
            while request_times and current_time - request_times[0] > 60:
                request_times.popleft()
            
            # Check burst protection
            if not self._check_burst_limit(client_ip, current_time):
                return False
            
            # Check if within rate limit
            if len(request_times) >= limit:
                return False
            
            # Add current request
            request_times.append(current_time)
            
            return True
    
    def _check_burst_limit(self, client_ip: str, current_time: float) -> bool:
        """
        Check burst protection (prevent rapid successive requests).
        """
        # Reset burst count if enough time has passed
        if current_time - self._burst_reset_times[client_ip] > 10:  # 10 second window
            self._burst_counts[client_ip] = 0
            self._burst_reset_times[client_ip] = current_time
        
        # Check burst limit
        if self._burst_counts[client_ip] >= self.burst_size:
            return False
        
        # Increment burst count
        self._burst_counts[client_ip] += 1
        
        return True
    
    async def _get_remaining_requests(self, client_ip: str, request: Request) -> int:
        """
        Get remaining requests for this client.
        """
        async with self._lock:
            limit = self._get_limit_for_request(request)
            current_requests = len(self._request_times[client_ip])
            return max(0, limit - current_requests)
    
    async def cleanup_old_entries(self):
        """
        Cleanup old entries to prevent memory leaks.
        This should be called periodically.
        """
        async with self._lock:
            current_time = time.time()
            
            # Clean request times
            for client_ip in list(self._request_times.keys()):
                request_times = self._request_times[client_ip]
                while request_times and current_time - request_times[0] > 60:
                    request_times.popleft()
                
                # Remove empty deques
                if not request_times:
                    del self._request_times[client_ip]
            
            # Clean burst counts
            for client_ip in list(self._burst_counts.keys()):
                if current_time - self._burst_reset_times[client_ip] > 60:
                    del self._burst_counts[client_ip]
                    del self._burst_reset_times[client_ip]