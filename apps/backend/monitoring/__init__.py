"""
Monitoring and observability module for La Vida Luca backend.
"""

from .logger import setup_logging, context_logger
from .metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    REQUEST_SIZE,
    RESPONSE_SIZE,
    ACTIVE_USERS,
    AI_REQUESTS,
    AI_LATENCY,
    DATABASE_CONNECTIONS,
    MEMORY_USAGE,
    CPU_USAGE,
    APP_INFO,
    update_system_metrics,
    record_ai_request,
    set_app_info,
    MetricsCollector,
)
from .sentry_config import (
    init_sentry,
    set_user_context,
    set_request_context,
    add_breadcrumb,
    capture_exception_with_context,
    capture_message_with_context,
)

__all__ = [
    # Logging
    "setup_logging",
    "context_logger",
    # Metrics
    "REQUEST_COUNT",
    "REQUEST_LATENCY",
    "REQUEST_SIZE",
    "RESPONSE_SIZE",
    "ACTIVE_USERS",
    "AI_REQUESTS",
    "AI_LATENCY",
    "DATABASE_CONNECTIONS",
    "MEMORY_USAGE",
    "CPU_USAGE",
    "APP_INFO",
    "update_system_metrics",
    "record_ai_request",
    "set_app_info",
    "MetricsCollector",
    # Sentry
    "init_sentry",
    "set_user_context",
    "set_request_context",
    "add_breadcrumb",
    "capture_exception_with_context",
    "capture_message_with_context",
]
