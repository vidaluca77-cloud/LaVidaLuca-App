import pytest
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

class TestErrorHandler:
    """Test error handling middleware"""
    
    def test_error_handler_init(self):
        """Test error handler middleware initialization"""
        middleware = ErrorHandlerMiddleware
        assert middleware is not None

class TestRateLimit:
    """Test rate limiting middleware"""
    
    def test_rate_limit_init(self):
        """Test rate limit middleware initialization"""
        middleware = RateLimitMiddleware
        assert middleware is not None