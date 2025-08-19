"""
Monitoring and metrics configuration
"""
import time
import logging
from typing import Optional
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from .config import settings

logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_database_connections',
    'Number of active database connections'
)

DB_QUERY_DURATION = Histogram(
    'database_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type']
)

ERROR_COUNT = Counter(
    'application_errors_total',
    'Total application errors',
    ['error_type', 'endpoint']
)

# Initialize Sentry
def init_sentry():
    """Initialize Sentry for error tracking"""
    if not settings.SENTRY_DSN:
        logger.warning("Sentry DSN not configured, error tracking disabled")
        return
    
    # Configure integrations
    integrations = [
        FastApiIntegration(auto_enable=True),
        SqlalchemyIntegration(),
        LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        ),
    ]
    
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENVIRONMENT or settings.ENVIRONMENT,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        sample_rate=settings.SENTRY_SAMPLE_RATE,
        integrations=integrations,
        send_default_pii=False,  # Don't send PII data
        attach_stacktrace=True,
        before_send=filter_errors,
        max_breadcrumbs=50,
    )
    
    # Set initial context
    sentry_sdk.set_context("app", {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    })
    
    logger.info("Sentry initialized successfully")

def filter_errors(event, hint):
    """Filter out non-critical errors"""
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        
        # Filter out expected errors
        if exc_type.__name__ in ['HTTPException', 'RequestValidationError']:
            return None
            
        # Filter out database connection errors during startup
        if 'connection' in str(exc_value).lower() and settings.is_development:
            return None
    
    # Add custom tags
    event.setdefault('tags', {})
    event['tags']['component'] = 'backend'
    event['tags']['environment'] = settings.ENVIRONMENT
    
    return event

# Metrics middleware
class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect metrics"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Get endpoint path template
        endpoint = self.get_endpoint_path(request)
        method = request.method
        
        try:
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            status = str(response.status_code)
            
            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status=status
            ).inc()
            
            REQUEST_DURATION.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
            
            return response
            
        except Exception as e:
            # Record error
            ERROR_COUNT.labels(
                error_type=type(e).__name__,
                endpoint=endpoint
            ).inc()
            
            # Set Sentry context
            sentry_sdk.set_context("request", {
                "method": method,
                "url": str(request.url),
                "endpoint": endpoint,
            })
            
            sentry_sdk.capture_exception(e)
            raise
    
    def get_endpoint_path(self, request: Request) -> str:
        """Get the endpoint path template"""
        # Try to get the route pattern
        if hasattr(request, 'scope') and 'route' in request.scope:
            route = request.scope['route']
            if hasattr(route, 'path'):
                return route.path
        
        # Fallback to path
        path = request.url.path
        
        # Normalize common patterns
        if path.startswith('/api/v1/'):
            return path
        elif path == '/metrics':
            return '/metrics'
        elif path == '/health':
            return '/health'
        else:
            return path

# Custom metrics functions
def record_db_query_time(query_type: str, duration: float):
    """Record database query duration"""
    DB_QUERY_DURATION.labels(query_type=query_type).observe(duration)

def update_active_connections(count: int):
    """Update active database connections gauge"""
    ACTIVE_CONNECTIONS.set(count)

def record_custom_metric(name: str, value: float, labels: Optional[dict] = None):
    """Record a custom metric"""
    try:
        # Create gauge for custom metrics
        gauge = Gauge(f'custom_{name}', f'Custom metric: {name}')
        if labels:
            gauge.labels(**labels).set(value)
        else:
            gauge.set(value)
    except Exception as e:
        logger.error(f"Failed to record custom metric {name}: {e}")

# Health check functions
async def get_health_metrics() -> dict:
    """Get application health metrics"""
    return {
        "sentry_enabled": bool(settings.SENTRY_DSN),
        "prometheus_enabled": settings.PROMETHEUS_ENABLED,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "version": settings.VERSION,
    }

def get_prometheus_metrics():
    """Get Prometheus metrics"""
    return generate_latest()

# Export metrics endpoint
def create_metrics_response():
    """Create metrics response for Prometheus"""
    from starlette.responses import Response
    return Response(
        content=get_prometheus_metrics(),
        media_type=CONTENT_TYPE_LATEST
    )