"""
Sentry configuration for La Vida Luca backend.
"""

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import os
from typing import Optional, Dict, Any


def init_sentry(
    dsn: Optional[str] = None,
    environment: str = "development",
    release: Optional[str] = None,
    traces_sample_rate: float = 1.0,
    profiles_sample_rate: float = 1.0,
):
    """
    Initialize Sentry for error tracking and performance monitoring.

    Args:
        dsn: Sentry DSN from environment or settings
        environment: Environment name (development, staging, production)
        release: Release version for tracking deployments
        traces_sample_rate: Percentage of transactions to sample for performance
        profiles_sample_rate: Percentage of transactions to profile
    """
    if not dsn:
        dsn = os.getenv("SENTRY_DSN")

    if not dsn:
        print("Sentry DSN not found, skipping Sentry initialization")
        return

    # Logging integration
    logging_integration = LoggingIntegration(
        level=None,  # Capture all log levels
        event_level=None,  # Don't send logs as events (we'll use structured logging)
    )

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        release=release,
        traces_sample_rate=traces_sample_rate,
        profiles_sample_rate=profiles_sample_rate,
        # Integrations
        integrations=[
            FastApiIntegration(auto_enable=True),
            SqlalchemyIntegration(),
            AsyncioIntegration(),
            logging_integration,
        ],
        # Performance
        enable_tracing=True,
        # Filter sensitive data
        before_send=filter_sensitive_data,
        before_send_transaction=filter_transaction_data,
        # Set initial context
        initial_scope={"tags": {"component": "backend", "service": "la-vida-luca-api"}},
    )


def filter_sensitive_data(
    event: Dict[str, Any], hint: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Filter sensitive data from Sentry events.

    Args:
        event: Sentry event data
        hint: Additional context

    Returns:
        Filtered event or None to drop the event
    """
    # Remove sensitive headers
    if "request" in event:
        headers = event["request"].get("headers", {})
        sensitive_headers = ["authorization", "cookie", "x-api-key"]
        for header in sensitive_headers:
            if header in headers:
                headers[header] = "[Filtered]"

    # Remove sensitive query parameters
    if "request" in event and "query_string" in event["request"]:
        # Basic filtering - in production, implement more sophisticated filtering
        query_string = event["request"]["query_string"]
        if "password" in query_string or "token" in query_string:
            event["request"]["query_string"] = "[Filtered]"

    return event


def filter_transaction_data(
    event: Dict[str, Any], hint: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Filter transaction data for performance monitoring.

    Args:
        event: Sentry transaction event
        hint: Additional context

    Returns:
        Filtered event or None to drop the transaction
    """
    # Filter out health check endpoints
    if "transaction" in event:
        transaction_name = event["transaction"]
        if transaction_name in ["/health", "/metrics", "/ready"]:
            return None

    return event


def set_user_context(
    user_id: str, email: Optional[str] = None, role: Optional[str] = None
):
    """
    Set user context for Sentry events.

    Args:
        user_id: User identifier
        email: User email address
        role: User role/permissions
    """
    sentry_sdk.set_user({"id": user_id, "email": email, "role": role})


def set_request_context(
    request_id: str, method: str, path: str, user_agent: Optional[str] = None
):
    """
    Set request context for Sentry events.

    Args:
        request_id: Unique request identifier
        method: HTTP method
        path: Request path
        user_agent: User agent string
    """
    sentry_sdk.set_context(
        "request",
        {
            "request_id": request_id,
            "method": method,
            "path": path,
            "user_agent": user_agent,
        },
    )


def add_breadcrumb(
    message: str,
    category: str = "custom",
    level: str = "info",
    data: Optional[Dict] = None,
):
    """
    Add breadcrumb for debugging context.

    Args:
        message: Breadcrumb message
        category: Category for grouping
        level: Log level
        data: Additional data
    """
    sentry_sdk.add_breadcrumb(
        message=message, category=category, level=level, data=data or {}
    )


def capture_exception_with_context(
    exception: Exception, context: Optional[Dict] = None, tags: Optional[Dict] = None
):
    """
    Capture exception with additional context.

    Args:
        exception: Exception to capture
        context: Additional context data
        tags: Tags for filtering and grouping
    """
    with sentry_sdk.push_scope() as scope:
        if context:
            scope.set_context("error_context", context)
        if tags:
            for key, value in tags.items():
                scope.set_tag(key, value)
        sentry_sdk.capture_exception(exception)


def capture_message_with_context(
    message: str,
    level: str = "info",
    context: Optional[Dict] = None,
    tags: Optional[Dict] = None,
):
    """
    Capture message with additional context.

    Args:
        message: Message to capture
        level: Message level
        context: Additional context data
        tags: Tags for filtering and grouping
    """
    with sentry_sdk.push_scope() as scope:
        if context:
            scope.set_context("message_context", context)
        if tags:
            for key, value in tags.items():
                scope.set_tag(key, value)
        sentry_sdk.capture_message(message, level=level)
