"""
Production monitoring configuration for La Vida Luca.
Integrates Sentry, Prometheus, and custom logging for comprehensive observability.
"""

import os
import logging
from typing import Optional
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from prometheus_client import start_http_server, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response, HTTPException
from fastapi.responses import PlainTextResponse
import asyncio
from datetime import datetime

# Configure logging
def setup_logging():
    """Set up structured logging for production."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure specific loggers
    loggers = {
        'uvicorn.access': logging.WARNING,
        'uvicorn.error': logging.INFO,
        'fastapi': logging.INFO,
        'sqlalchemy.engine': logging.WARNING if log_level != 'DEBUG' else logging.INFO
    }
    
    for logger_name, level in loggers.items():
        logging.getLogger(logger_name).setLevel(level)
    
    return logging.getLogger(__name__)

logger = setup_logging()

def setup_sentry(environment: str = None):
    """
    Initialize Sentry for error tracking and performance monitoring.
    
    Args:
        environment: Deployment environment (development, staging, production)
    """
    sentry_dsn = os.getenv("SENTRY_DSN")
    if not sentry_dsn or sentry_dsn == "your-sentry-dsn-here":
        logger.warning("Sentry DSN not configured, skipping Sentry initialization")
        return
    
    environment = environment or os.getenv("ENVIRONMENT", "development")
    
    # Configure Sentry integrations
    integrations = [
        FastApiIntegration(auto_enabling_integrations=False),
        SqlalchemyIntegration(),
        LoggingIntegration(
            level=logging.INFO,        # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        ),
    ]
    
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=environment,
        integrations=integrations,
        traces_sample_rate=1.0 if environment == "development" else 0.1,
        send_default_pii=False,  # Don't send personally identifiable information
        attach_stacktrace=True,
        debug=environment == "development",
        release=os.getenv("APP_VERSION", "1.0.0"),
        before_send=filter_sentry_events,
        before_send_transaction=filter_sentry_transactions,
    )
    
    logger.info(f"Sentry initialized for environment: {environment}")

def filter_sentry_events(event, hint):
    """
    Filter Sentry events to reduce noise.
    
    Args:
        event: Sentry event data
        hint: Additional context
        
    Returns:
        Modified event or None to discard
    """
    # Skip health check errors
    if event.get('request', {}).get('url', '').endswith('/health'):
        return None
    
    # Skip 404 errors for common bot requests
    if event.get('request', {}).get('url', '').endswith(('.php', '.xml', '.txt')):
        return None
    
    return event

def filter_sentry_transactions(event, hint):
    """
    Filter Sentry transactions to reduce quota usage.
    
    Args:
        event: Sentry transaction event
        hint: Additional context
        
    Returns:
        Modified event or None to discard
    """
    # Skip health check transactions
    transaction_name = event.get('transaction', '')
    if any(health_path in transaction_name for health_path in ['/health', '/metrics']):
        return None
    
    return event

class PrometheusExporter:
    """Prometheus metrics exporter for FastAPI."""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.server_started = False
    
    async def start_server(self):
        """Start Prometheus metrics server."""
        if not self.server_started:
            try:
                start_http_server(self.port)
                self.server_started = True
                logger.info(f"Prometheus metrics server started on port {self.port}")
            except Exception as e:
                logger.error(f"Failed to start Prometheus server: {e}")
    
    def get_metrics_endpoint(self):
        """Return FastAPI endpoint for serving Prometheus metrics."""
        async def metrics():
            """Serve Prometheus metrics."""
            try:
                metrics_data = generate_latest()
                return Response(
                    content=metrics_data,
                    media_type=CONTENT_TYPE_LATEST
                )
            except Exception as e:
                logger.error(f"Error generating metrics: {e}")
                raise HTTPException(status_code=500, detail="Error generating metrics")
        
        return metrics

class HealthMetrics:
    """Health and performance metrics collector."""
    
    def __init__(self):
        self.startup_time = datetime.utcnow()
        self.request_count = 0
        self.error_count = 0
    
    def record_request(self):
        """Record a new request."""
        self.request_count += 1
    
    def record_error(self):
        """Record an error."""
        self.error_count += 1
    
    def get_uptime_seconds(self) -> float:
        """Get application uptime in seconds."""
        return (datetime.utcnow() - self.startup_time).total_seconds()
    
    def get_error_rate(self) -> float:
        """Get current error rate."""
        if self.request_count == 0:
            return 0.0
        return self.error_count / self.request_count

# Global health metrics instance
health_metrics = HealthMetrics()

async def monitoring_middleware(request: Request, call_next):
    """
    Monitoring middleware to collect request metrics and errors.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/handler
        
    Returns:
        Response with monitoring data collected
    """
    health_metrics.record_request()
    
    try:
        response = await call_next(request)
        
        # Record error if status code indicates an error
        if response.status_code >= 400:
            health_metrics.record_error()
            
            # Log API errors for monitoring
            if response.status_code >= 500:
                logger.error(
                    f"API Error: {request.method} {request.url.path} "
                    f"returned {response.status_code}"
                )
        
        return response
        
    except Exception as e:
        health_metrics.record_error()
        logger.error(f"Unhandled error in {request.method} {request.url.path}: {str(e)}")
        raise

class AlertManager:
    """Manages alerts and notifications for critical issues."""
    
    def __init__(self):
        self.alert_thresholds = {
            'error_rate': 0.1,  # 10%
            'response_time': 5.0,  # 5 seconds
            'memory_usage': 0.9,  # 90%
            'cpu_usage': 0.8,  # 80%
        }
    
    async def check_alerts(self):
        """Check for alert conditions and trigger notifications."""
        alerts = []
        
        # Check error rate
        error_rate = health_metrics.get_error_rate()
        if error_rate > self.alert_thresholds['error_rate']:
            alerts.append({
                'type': 'error_rate',
                'severity': 'high',
                'message': f'Error rate is {error_rate:.2%}, above threshold of {self.alert_thresholds["error_rate"]:.2%}',
                'value': error_rate
            })
        
        # Additional checks would go here (memory, CPU, etc.)
        
        if alerts:
            await self.send_alerts(alerts)
    
    async def send_alerts(self, alerts: list):
        """
        Send alerts to configured channels.
        
        Args:
            alerts: List of alert dictionaries
        """
        for alert in alerts:
            logger.critical(
                f"ALERT: {alert['type']} - {alert['message']}",
                extra={'alert': alert}
            )
            
            # In production, you would send to Slack, email, etc.
            # For now, we log and send to Sentry
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("alert_type", alert['type'])
                scope.set_level("error")
                sentry_sdk.capture_message(
                    f"Production Alert: {alert['message']}",
                    level="error"
                )

# Global alert manager
alert_manager = AlertManager()

async def periodic_monitoring():
    """Background task for periodic monitoring checks."""
    while True:
        try:
            await alert_manager.check_alerts()
            await asyncio.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"Error in periodic monitoring: {e}")
            await asyncio.sleep(60)

def setup_monitoring(app, environment: str = None):
    """
    Set up comprehensive monitoring for the FastAPI application.
    
    Args:
        app: FastAPI application instance
        environment: Deployment environment
    """
    environment = environment or os.getenv("ENVIRONMENT", "development")
    
    # Initialize Sentry
    setup_sentry(environment)
    
    # Add monitoring middleware
    app.middleware("http")(monitoring_middleware)
    
    # Set up Prometheus metrics
    if environment == "production":
        prometheus = PrometheusExporter()
        
        @app.on_event("startup")
        async def start_prometheus():
            await prometheus.start_server()
        
        # Add metrics endpoint
        app.get("/metrics", response_class=PlainTextResponse)(
            prometheus.get_metrics_endpoint()
        )
    
    # Start background monitoring
    @app.on_event("startup")
    async def start_monitoring():
        if environment == "production":
            asyncio.create_task(periodic_monitoring())
    
    logger.info(f"Monitoring configured for environment: {environment}")

# Export configuration functions
__all__ = [
    'setup_monitoring',
    'setup_sentry', 
    'setup_logging',
    'health_metrics',
    'alert_manager'
]