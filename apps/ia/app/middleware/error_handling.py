"""
Error handling middleware.
"""
import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware to handle errors and exceptions globally."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        
        except HTTPException as exc:
            # FastAPI HTTPExceptions are handled normally
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
        
        except Exception as exc:
            # Log the error
            logger.error(f"Unhandled exception: {str(exc)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Return a generic error response
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "error": str(exc) if logger.level <= logging.DEBUG else "An unexpected error occurred"
                }
            )


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log requests and responses."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Log request
        logger.info(f"{request.method} {request.url.path} - {request.client.host if request.client else 'Unknown'}")
        
        # Process request
        response = await call_next(request)
        
        # Log response
        logger.info(f"Response: {response.status_code}")
        
        return response