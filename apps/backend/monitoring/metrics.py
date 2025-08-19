"""
Prometheus metrics for La Vida Luca backend.
Provides request metrics, custom counters, and performance monitoring.
"""

from prometheus_client import Counter, Histogram, Gauge, Info
from fastapi import Request, Response
import time
import psutil
import os

# HTTP Request metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

REQUEST_SIZE = Histogram(
    "http_request_size_bytes",
    "HTTP request size in bytes",
    ["method", "endpoint"]
)

RESPONSE_SIZE = Histogram(
    "http_response_size_bytes", 
    "HTTP response size in bytes",
    ["method", "endpoint"]
)

# Application metrics
ACTIVE_USERS = Gauge(
    "active_users_total",
    "Number of currently active users"
)

AI_REQUESTS = Counter(
    "ai_requests_total",
    "Total AI/OpenAI requests",
    ["type", "status"]
)

AI_LATENCY = Histogram(
    "ai_request_duration_seconds",
    "AI request latency in seconds",
    ["type"]
)

DATABASE_CONNECTIONS = Gauge(
    "database_connections_active",
    "Number of active database connections"
)

# System metrics
MEMORY_USAGE = Gauge(
    "memory_usage_bytes",
    "Memory usage in bytes"
)

CPU_USAGE = Gauge(
    "cpu_usage_percent",
    "CPU usage percentage"
)

# Application info
APP_INFO = Info(
    "app_info",
    "Application information"
)

async def metrics_middleware(request: Request, call_next):
    """
    FastAPI middleware to collect HTTP metrics.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/handler in chain
        
    Returns:
        Response with metrics recorded
    """
    start_time = time.time()
    
    # Record request size
    content_length = request.headers.get("content-length")
    if content_length:
        REQUEST_SIZE.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(int(content_length))
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Record metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    # Record response size if available
    if hasattr(response, "body"):
        response_size = len(response.body)
        RESPONSE_SIZE.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(response_size)
    
    return response

def update_system_metrics():
    """Update system-level metrics."""
    try:
        # Memory usage
        memory = psutil.virtual_memory()
        MEMORY_USAGE.set(memory.used)
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        CPU_USAGE.set(cpu_percent)
        
    except Exception as e:
        # Log error but don't fail
        print(f"Failed to update system metrics: {e}")

def record_ai_request(request_type: str, duration: float, success: bool = True):
    """
    Record AI request metrics.
    
    Args:
        request_type: Type of AI request (e.g., 'completion', 'embedding')
        duration: Request duration in seconds
        success: Whether the request was successful
    """
    status = "success" if success else "error"
    
    AI_REQUESTS.labels(
        type=request_type,
        status=status
    ).inc()
    
    AI_LATENCY.labels(type=request_type).observe(duration)

def set_app_info(version: str, environment: str, build_date: str):
    """Set application information metrics."""
    APP_INFO.info({
        "version": version,
        "environment": environment,
        "build_date": build_date,
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
    })

class MetricsCollector:
    """Context manager for collecting custom metrics."""
    
    def __init__(self, metric_name: str, labels: dict = None):
        self.metric_name = metric_name
        self.labels = labels or {}
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            
            # Record to appropriate metric based on name
            if "latency" in self.metric_name.lower():
                if hasattr(globals(), self.metric_name.upper()):
                    metric = globals()[self.metric_name.upper()]
                    if self.labels:
                        metric.labels(**self.labels).observe(duration)
                    else:
                        metric.observe(duration)