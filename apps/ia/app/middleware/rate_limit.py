from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
from typing import Dict
from app.core.config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = None):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute or settings.RATE_LIMIT_REQUESTS
        self.window_size = settings.RATE_LIMIT_WINDOW
        self.clients: Dict[str, list] = {}
    
    def get_client_ip(self, request: Request) -> str:
        # Get client IP from headers (for reverse proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    def is_rate_limited(self, client_ip: str) -> bool:
        current_time = time.time()
        
        # Initialize client if not exists
        if client_ip not in self.clients:
            self.clients[client_ip] = []
        
        # Remove old requests outside the window
        self.clients[client_ip] = [
            req_time for req_time in self.clients[client_ip]
            if current_time - req_time < self.window_size
        ]
        
        # Check if rate limit exceeded
        if len(self.clients[client_ip]) >= self.requests_per_minute:
            return True
        
        # Add current request
        self.clients[client_ip].append(current_time)
        return False
    
    async def dispatch(self, request: Request, call_next):
        client_ip = self.get_client_ip(request)
        
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc"]:
            return await call_next(request)
        
        if self.is_rate_limited(client_ip):
            return JSONResponse(
                status_code=429,
                content={
                    "error": True,
                    "message": "Trop de requêtes, veuillez réessayer plus tard",
                    "status_code": 429
                }
            )
        
        return await call_next(request)