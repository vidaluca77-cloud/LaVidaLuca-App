"""
Health check and validation endpoints for La Vida Luca backend.
Provides comprehensive health monitoring for production deployments.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
import time
import asyncio
import psutil
from datetime import datetime, timezone
import aiohttp
import asyncpg

router = APIRouter(tags=["health"])


class HealthStatus(BaseModel):
    """Health status response model."""
    status: str
    timestamp: str
    environment: str
    version: str
    checks: Dict[str, Any]


class ValidationResult(BaseModel):
    """Validation result model."""
    service: str
    status: str
    message: str
    duration_ms: float
    details: Optional[Dict[str, Any]] = None


class SystemMetrics(BaseModel):
    """System metrics response model."""
    cpu_percent: float
    memory_usage: Dict[str, Any]
    disk_usage: Dict[str, Any]
    uptime_seconds: float


async def check_database() -> ValidationResult:
    """Check database connectivity."""
    start_time = time.time()
    
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return ValidationResult(
                service="database",
                status="error",
                message="DATABASE_URL not configured",
                duration_ms=(time.time() - start_time) * 1000
            )
        
        # Try to connect to database
        conn = await asyncpg.connect(database_url)
        result = await conn.fetchval("SELECT 1")
        await conn.close()
        
        return ValidationResult(
            service="database",
            status="healthy",
            message="Database connection successful",
            duration_ms=(time.time() - start_time) * 1000,
            details={"query_result": result}
        )
        
    except Exception as e:
        return ValidationResult(
            service="database",
            status="error",
            message=f"Database connection failed: {str(e)}",
            duration_ms=(time.time() - start_time) * 1000
        )


async def check_openai() -> ValidationResult:
    """Check OpenAI API connectivity."""
    start_time = time.time()
    
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return ValidationResult(
                service="openai",
                status="warning",
                message="OPENAI_API_KEY not configured",
                duration_ms=(time.time() - start_time) * 1000
            )
        
        if api_key == "your-openai-api-key-here":
            return ValidationResult(
                service="openai",
                status="warning",
                message="OPENAI_API_KEY is using example value",
                duration_ms=(time.time() - start_time) * 1000
            )
        
        # Test API connectivity with a simple request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.openai.com/v1/models",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    return ValidationResult(
                        service="openai",
                        status="healthy",
                        message="OpenAI API accessible",
                        duration_ms=(time.time() - start_time) * 1000
                    )
                else:
                    return ValidationResult(
                        service="openai",
                        status="error",
                        message=f"OpenAI API returned status {response.status}",
                        duration_ms=(time.time() - start_time) * 1000
                    )
                    
    except asyncio.TimeoutError:
        return ValidationResult(
            service="openai",
            status="error",
            message="OpenAI API request timed out",
            duration_ms=(time.time() - start_time) * 1000
        )
    except Exception as e:
        return ValidationResult(
            service="openai",
            status="error",
            message=f"OpenAI API check failed: {str(e)}",
            duration_ms=(time.time() - start_time) * 1000
        )


async def check_environment() -> ValidationResult:
    """Check environment configuration."""
    start_time = time.time()
    
    required_vars = [
        "ENVIRONMENT",
        "JWT_SECRET_KEY",
        "DATABASE_URL"
    ]
    
    missing_vars = []
    example_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        elif "example" in value.lower() or "your-" in value.lower():
            example_vars.append(var)
    
    status = "healthy"
    messages = []
    
    if missing_vars:
        status = "error"
        messages.append(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    if example_vars:
        status = "warning" if status == "healthy" else status
        messages.append(f"Environment variables using example values: {', '.join(example_vars)}")
    
    if not messages:
        messages.append("All required environment variables are configured")
    
    return ValidationResult(
        service="environment",
        status=status,
        message="; ".join(messages),
        duration_ms=(time.time() - start_time) * 1000,
        details={
            "environment": os.getenv("ENVIRONMENT", "unknown"),
            "required_vars": required_vars,
            "missing_vars": missing_vars,
            "example_vars": example_vars
        }
    )


def get_system_metrics() -> SystemMetrics:
    """Get current system metrics."""
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Memory usage
    memory = psutil.virtual_memory()
    memory_usage = {
        "total_gb": round(memory.total / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2),
        "used_gb": round(memory.used / (1024**3), 2),
        "percent": memory.percent
    }
    
    # Disk usage
    disk = psutil.disk_usage('/')
    disk_usage = {
        "total_gb": round(disk.total / (1024**3), 2),
        "free_gb": round(disk.free / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "percent": round((disk.used / disk.total) * 100, 2)
    }
    
    # System uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    
    return SystemMetrics(
        cpu_percent=cpu_percent,
        memory_usage=memory_usage,
        disk_usage=disk_usage,
        uptime_seconds=uptime_seconds
    )


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Comprehensive health check endpoint.
    Returns overall application health status.
    """
    start_time = time.time()
    
    # Run all health checks
    checks = {}
    
    # Environment check
    env_result = await check_environment()
    checks["environment"] = env_result.dict()
    
    # Database check
    db_result = await check_database()
    checks["database"] = db_result.dict()
    
    # OpenAI check
    openai_result = await check_openai()
    checks["openai"] = openai_result.dict()
    
    # System metrics
    system_metrics = get_system_metrics()
    checks["system"] = system_metrics.dict()
    
    # Determine overall status
    statuses = [env_result.status, db_result.status, openai_result.status]
    if "error" in statuses:
        overall_status = "unhealthy"
    elif "warning" in statuses:
        overall_status = "degraded"
    else:
        overall_status = "healthy"
    
    checks["overall"] = {
        "status": overall_status,
        "duration_ms": (time.time() - start_time) * 1000
    }
    
    return HealthStatus(
        status=overall_status,
        timestamp=datetime.now(timezone.utc).isoformat(),
        environment=os.getenv("ENVIRONMENT", "unknown"),
        version=os.getenv("APP_VERSION", "1.0.0"),
        checks=checks
    )


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes/container orchestration.
    Returns 200 if the app is ready to serve traffic.
    """
    # Check critical dependencies
    env_result = await check_environment()
    db_result = await check_database()
    
    if env_result.status == "error" or db_result.status == "error":
        raise HTTPException(status_code=503, detail="Service not ready")
    
    return {"status": "ready", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/health/live")
async def liveness_check():
    """
    Liveness check for Kubernetes/container orchestration.
    Returns 200 if the app is alive (even if not fully healthy).
    """
    return {
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pid": os.getpid()
    }


@router.get("/health/detailed", response_model=List[ValidationResult])
async def detailed_health_check():
    """
    Detailed health check with individual service results.
    Useful for debugging and monitoring.
    """
    results = []
    
    # Run all checks in parallel
    checks = await asyncio.gather(
        check_environment(),
        check_database(),
        check_openai(),
        return_exceptions=True
    )
    
    for check in checks:
        if isinstance(check, ValidationResult):
            results.append(check)
        else:
            # Handle any unexpected errors
            results.append(ValidationResult(
                service="unknown",
                status="error",
                message=f"Health check failed: {str(check)}",
                duration_ms=0
            ))
    
    return results


@router.get("/metrics/system", response_model=SystemMetrics)
async def system_metrics():
    """
    Get current system metrics.
    Useful for monitoring resource usage.
    """
    return get_system_metrics()


@router.get("/validate/deployment")
async def validate_deployment():
    """
    Comprehensive deployment validation.
    Checks all critical components for production readiness.
    """
    validation_results = []
    overall_success = True
    
    # Get detailed health results
    health_results = await detailed_health_check()
    
    for result in health_results:
        validation_results.append({
            "component": result.service,
            "status": result.status,
            "message": result.message,
            "success": result.status in ["healthy", "warning"]
        })
        
        if result.status == "error":
            overall_success = False
    
    # Additional production-specific checks
    production_checks = [
        {
            "component": "security_headers",
            "check": lambda: os.getenv("ENVIRONMENT") == "production",
            "message": "Production environment configured"
        },
        {
            "component": "jwt_secret",
            "check": lambda: len(os.getenv("JWT_SECRET_KEY", "")) >= 32,
            "message": "JWT secret key is sufficiently long"
        },
        {
            "component": "cors_origins",
            "check": lambda: os.getenv("CORS_ORIGINS") and "localhost" not in os.getenv("CORS_ORIGINS", ""),
            "message": "CORS origins configured for production"
        }
    ]
    
    for check in production_checks:
        try:
            success = check["check"]()
            validation_results.append({
                "component": check["component"],
                "status": "pass" if success else "fail",
                "message": check["message"],
                "success": success
            })
            if not success:
                overall_success = False
        except Exception as e:
            validation_results.append({
                "component": check["component"],
                "status": "error",
                "message": f"Check failed: {str(e)}",
                "success": False
            })
            overall_success = False
    
    return {
        "deployment_valid": overall_success,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "checks": validation_results
    }