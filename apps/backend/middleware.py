"""
Middleware setup for the FastAPI application.
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
import uuid
import json
from typing import Callable

from .config import settings
from .monitoring.logger import context_logger
from .monitoring.metrics import metrics_middleware
from .monitoring.sentry_config import set_request_context, add_breadcrumb

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI):
    """Setup all middleware for the application."""
    
    # Add metrics middleware first
    app.middleware("http")(metrics_middleware)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    if settings.ENVIRONMENT == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.TRUSTED_HOSTS
        )
    
    # Request tracking middleware
    @app.middleware("http")
    async def request_tracking_middleware(request: Request, call_next: Callable):
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Get client info
        client_ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown")
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Set request context for monitoring
        set_request_context(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            user_agent=user_agent
        )
        
        # Set logging context
        context_logger.set_context(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=client_ip,
            user_agent=user_agent
        )
        
        start_time = time.time()
        
        # Log request start
        context_logger.info("Request started", 
            url=str(request.url),
            query_params=dict(request.query_params),
            headers={k: v for k, v in request.headers.items() if k.lower() not in ['authorization', 'cookie']}
        )
        
        # Add breadcrumb for Sentry
        add_breadcrumb(
            message=f"Request started: {request.method} {request.url.path}",
            category="http.request",
            level="info",
            data={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": client_ip
            }
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Add response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{duration:.3f}"
            
            # Log successful response
            context_logger.info("Request completed successfully",
                status_code=response.status_code,
                duration_ms=duration * 1000,
                response_size=response.headers.get("content-length", 0)
            )
            
            # Add breadcrumb for response
            add_breadcrumb(
                message=f"Request completed: {response.status_code}",
                category="http.response",
                level="info",
                data={
                    "status_code": response.status_code,
                    "duration_ms": duration * 1000
                }
            )
            
            # Log slow requests
            if duration > 1.0:
                context_logger.warning("Slow request detected",
                    duration_ms=duration * 1000,
                    threshold_ms=1000
                )
            
            return response
            
        except Exception as e:
            # Calculate duration for failed requests
            duration = time.time() - start_time
            
            # Log error
            context_logger.error("Request failed",
                error=str(e),
                error_type=type(e).__name__,
                duration_ms=duration * 1000
            )
            
            # Add breadcrumb for error
            add_breadcrumb(
                message=f"Request failed: {type(e).__name__}",
                category="http.error",
                level="error",
                data={
                    "error": str(e),
                    "duration_ms": duration * 1000
                }
            )
            
            # Re-raise exception to be handled by FastAPI
            raise
        
        finally:
            # Clear request context
            context_logger.clear_context()
    
    # User activity tracking middleware
    @app.middleware("http")
    async def activity_tracking_middleware(request: Request, call_next: Callable):
        # Skip tracking for health checks and static assets
        skip_paths = ['/health', '/metrics', '/docs', '/redoc', '/openapi.json']
        if any(request.url.path.startswith(path) for path in skip_paths):
            return await call_next(request)
        
        # Track user activity based on path
        activity_type = classify_activity(request.method, request.url.path)
        
        if activity_type:
            add_breadcrumb(
                message=f"User activity: {activity_type}",
                category="user.activity",
                level="info",
                data={
                    "activity_type": activity_type,
                    "path": request.url.path,
                    "method": request.method
                }
            )
        
        return await call_next(request)

def classify_activity(method: str, path: str) -> str:
    """
    Classify user activity based on HTTP method and path.
    
    Args:
        method: HTTP method
        path: Request path
        
    Returns:
        Activity type string
    """
    # Catalogue activities
    if '/catalogue' in path:
        if method == 'GET':
            return 'catalogue_browse'
        elif method == 'POST':
            return 'catalogue_create'
        elif method in ['PUT', 'PATCH']:
            return 'catalogue_update'
        elif method == 'DELETE':
            return 'catalogue_delete'
    
    # Authentication activities
    if '/auth' in path:
        if 'login' in path:
            return 'user_login'
        elif 'register' in path:
            return 'user_register'
        elif 'logout' in path:
            return 'user_logout'
    
    # Contact activities
    if '/contact' in path and method == 'POST':
        return 'contact_submit'
    
    # Rejoindre activities
    if '/rejoindre' in path and method == 'POST':
        return 'rejoindre_submit'
    
    # AI activities
    if '/ai' in path or '/openai' in path:
        return 'ai_request'
    
    # Generic CRUD operations
    if method == 'GET':
        return 'data_read'
    elif method == 'POST':
        return 'data_create'
    elif method in ['PUT', 'PATCH']:
        return 'data_update'
    elif method == 'DELETE':
        return 'data_delete'
    
    return 'unknown_activity'