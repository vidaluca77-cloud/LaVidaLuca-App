"""
Tests for backend monitoring functionality
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import Request, Response
from fastapi.testclient import TestClient

from apps.backend.monitoring.sentry_config import (
    init_sentry, set_user_context, set_request_context, 
    capture_exception_with_context, filter_sensitive_data
)
from apps.backend.monitoring.logger import setup_logging, ContextLogger
from apps.backend.monitoring.metrics import (
    record_ai_request, MetricsCollector, update_system_metrics
)
from apps.backend.middleware import classify_activity


class TestSentryConfig:
    """Test Sentry configuration functions."""
    
    @patch('apps.backend.monitoring.sentry_config.sentry_sdk')
    def test_init_sentry_with_dsn(self, mock_sentry):
        """Test Sentry initialization with DSN."""
        init_sentry(dsn="test-dsn", environment="test")
        mock_sentry.init.assert_called_once()
        
    @patch('apps.backend.monitoring.sentry_config.sentry_sdk')
    @patch('apps.backend.monitoring.sentry_config.os.getenv')
    def test_init_sentry_without_dsn(self, mock_getenv, mock_sentry):
        """Test Sentry initialization without DSN."""
        mock_getenv.return_value = None
        init_sentry()
        mock_sentry.init.assert_not_called()
        
    @patch('apps.backend.monitoring.sentry_config.sentry_sdk')
    def test_set_user_context(self, mock_sentry):
        """Test setting user context."""
        set_user_context(
            user_id="123",
            email="test@example.com",
            role="user"
        )
        mock_sentry.set_user.assert_called_once_with({
            "id": "123",
            "email": "test@example.com",
            "role": "user"
        })
        
    @patch('apps.backend.monitoring.sentry_config.sentry_sdk')
    def test_set_request_context(self, mock_sentry):
        """Test setting request context."""
        set_request_context(
            request_id="req-123",
            method="POST",
            path="/api/test",
            user_agent="test-agent"
        )
        mock_sentry.set_context.assert_called_once_with("request", {
            "request_id": "req-123",
            "method": "POST",
            "path": "/api/test",
            "user_agent": "test-agent"
        })
        
    def test_filter_sensitive_data(self):
        """Test filtering sensitive data from events."""
        event = {
            'request': {
                'headers': {
                    'authorization': 'Bearer token',
                    'cookie': 'session=abc',
                    'content-type': 'application/json'
                },
                'query_string': 'password=secret&user=test'
            }
        }
        
        filtered = filter_sensitive_data(event, {})
        
        assert filtered['request']['headers']['authorization'] == '[Filtered]'
        assert filtered['request']['headers']['cookie'] == '[Filtered]'
        assert filtered['request']['headers']['content-type'] == 'application/json'
        assert filtered['request']['query_string'] == '[Filtered]'
        
    @patch('apps.backend.monitoring.sentry_config.sentry_sdk')
    def test_capture_exception_with_context(self, mock_sentry):
        """Test capturing exception with context."""
        exception = Exception("Test error")
        context = {"key": "value"}
        tags = {"tag1": "value1"}
        
        mock_scope = MagicMock()
        mock_sentry.push_scope.return_value.__enter__.return_value = mock_scope
        
        capture_exception_with_context(exception, context, tags)
        
        mock_scope.set_context.assert_called_once_with("error_context", context)
        mock_scope.set_tag.assert_called_once_with("tag1", "value1")
        mock_sentry.capture_exception.assert_called_once_with(exception)


class TestLogger:
    """Test logging functionality."""
    
    def test_setup_logging(self):
        """Test logger setup."""
        logger = setup_logging("test-service")
        assert logger.name == "test-service"
        
    def test_context_logger(self):
        """Test context logger functionality."""
        import logging
        base_logger = logging.getLogger("test")
        context_logger = ContextLogger(base_logger)
        
        # Test setting context
        context_logger.set_context(user_id="123", request_id="req-456")
        assert context_logger.context["user_id"] == "123"
        assert context_logger.context["request_id"] == "req-456"
        
        # Test clearing context
        context_logger.clear_context()
        assert len(context_logger.context) == 0


class TestMetrics:
    """Test metrics functionality."""
    
    @patch('apps.backend.monitoring.metrics.AI_REQUESTS')
    @patch('apps.backend.monitoring.metrics.AI_LATENCY')
    def test_record_ai_request(self, mock_latency, mock_requests):
        """Test recording AI request metrics."""
        record_ai_request("completion", 1.5, True)
        
        mock_requests.labels.assert_called_once_with(
            type="completion",
            status="success"
        )
        mock_latency.labels.assert_called_once_with(type="completion")
        
    @patch('apps.backend.monitoring.metrics.psutil')
    def test_update_system_metrics(self, mock_psutil):
        """Test updating system metrics."""
        # Mock psutil calls
        mock_memory = MagicMock()
        mock_memory.used = 1024 * 1024 * 1024  # 1GB
        mock_psutil.virtual_memory.return_value = mock_memory
        mock_psutil.cpu_percent.return_value = 50.0
        
        # This should not raise an exception
        update_system_metrics()
        
        mock_psutil.virtual_memory.assert_called_once()
        mock_psutil.cpu_percent.assert_called_once_with(interval=1)
        
    def test_metrics_collector(self):
        """Test metrics collector context manager."""
        with patch('apps.backend.monitoring.metrics.time') as mock_time:
            mock_time.time.side_effect = [1000.0, 1001.5]  # 1.5 second duration
            
            with MetricsCollector("test_metric") as collector:
                pass  # Simulate some work
                
            # Verify timing was recorded
            assert collector.start_time == 1000.0


class TestMiddleware:
    """Test middleware functionality."""
    
    def test_classify_activity_catalogue(self):
        """Test activity classification for catalogue operations."""
        assert classify_activity("GET", "/api/v1/catalogue") == "catalogue_browse"
        assert classify_activity("POST", "/api/v1/catalogue") == "catalogue_create"
        assert classify_activity("PUT", "/api/v1/catalogue/123") == "catalogue_update"
        assert classify_activity("DELETE", "/api/v1/catalogue/123") == "catalogue_delete"
        
    def test_classify_activity_auth(self):
        """Test activity classification for auth operations."""
        assert classify_activity("POST", "/api/v1/auth/login") == "user_login"
        assert classify_activity("POST", "/api/v1/auth/register") == "user_register"
        assert classify_activity("POST", "/api/v1/auth/logout") == "user_logout"
        
    def test_classify_activity_contact(self):
        """Test activity classification for contact operations."""
        assert classify_activity("POST", "/api/v1/contact") == "contact_submit"
        assert classify_activity("POST", "/api/v1/rejoindre") == "rejoindre_submit"
        
    def test_classify_activity_ai(self):
        """Test activity classification for AI operations."""
        assert classify_activity("POST", "/api/v1/ai/completion") == "ai_request"
        assert classify_activity("GET", "/api/v1/openai/models") == "ai_request"
        
    def test_classify_activity_generic(self):
        """Test activity classification for generic operations."""
        assert classify_activity("GET", "/api/v1/unknown") == "data_read"
        assert classify_activity("POST", "/api/v1/unknown") == "data_create"
        assert classify_activity("PUT", "/api/v1/unknown") == "data_update"
        assert classify_activity("DELETE", "/api/v1/unknown") == "data_delete"


@pytest.mark.asyncio
class TestMonitoringIntegration:
    """Integration tests for monitoring features."""
    
    def test_metrics_endpoint_exists(self):
        """Test that metrics endpoint is available."""
        from apps.backend.main import app
        client = TestClient(app)
        
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        
    def test_health_check_includes_monitoring(self):
        """Test that health check works with monitoring."""
        from apps.backend.main import app
        client = TestClient(app)
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert "environment" in data
        
    @patch('apps.backend.monitoring.sentry_config.sentry_sdk')
    def test_request_tracking_with_monitoring(self, mock_sentry):
        """Test that requests are properly tracked."""
        from apps.backend.main import app
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
        
        # Check that request ID was added
        assert "X-Request-ID" in response.headers
        assert "X-Process-Time" in response.headers
        
        # Verify Sentry breadcrumb was added
        mock_sentry.add_breadcrumb.assert_called()


if __name__ == "__main__":
    pytest.main([__file__])