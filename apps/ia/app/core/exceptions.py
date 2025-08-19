"""
Exception handlers and custom exceptions
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class BaseAPIException(Exception):
    """Base exception for API errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class UserNotFoundError(BaseAPIException):
    """User not found exception"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, 404)


class ActivityNotFoundError(BaseAPIException):
    """Activity not found exception"""
    def __init__(self, message: str = "Activity not found"):
        super().__init__(message, 404)


class AuthenticationError(BaseAPIException):
    """Authentication exception"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


async def base_exception_handler(request: Request, exc: BaseAPIException):
    """Handle custom API exceptions"""
    logger.error(f"API Exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "type": exc.__class__.__name__}
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle SQLAlchemy exceptions"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred", "type": "DatabaseError"}
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "InternalError"}
    )


def setup_exception_handlers(app: FastAPI):
    """Set up exception handlers for the FastAPI app"""
    app.add_exception_handler(BaseAPIException, base_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)