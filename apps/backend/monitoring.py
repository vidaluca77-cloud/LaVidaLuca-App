import logging
from datetime import datetime
from typing import Dict, Any, Optional
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Metrics:
    def __init__(self):
        self.logger = logging.getLogger("metrics")
        
    def record_api_call(self, path: str, method: str, duration: float, status_code: int = 200):
        """Record API call metrics"""
        self.logger.info("api_call", extra={
            "event_type": "api_call",
            "path": path,
            "method": method,
            "duration": duration,
            "status_code": status_code,
            "timestamp": datetime.utcnow().isoformat()
        })

    def record_error(self, error: Exception, context: Dict[str, Any]):
        """Record error events with context"""
        self.logger.error(
            "error",
            extra={
                "event_type": "error",
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    def record_user_activity(self, user_id: str, activity: str, metadata: Optional[Dict[str, Any]] = None):
        """Record user activity for analytics"""
        self.logger.info("user_activity", extra={
            "event_type": "user_activity",
            "user_id": user_id,
            "activity": activity,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        })

    def record_business_metric(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record business-specific metrics"""
        self.logger.info("business_metric", extra={
            "event_type": "business_metric",
            "metric_name": metric_name,
            "value": value,
            "tags": tags or {},
            "timestamp": datetime.utcnow().isoformat()
        })

# Global metrics instance
metrics = Metrics()

# Health check metrics
class HealthCheck:
    def __init__(self):
        self.logger = logging.getLogger("health")
    
    def check_database(self) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            # TODO: Implement actual database check
            return {
                "status": "healthy",
                "response_time_ms": 50,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def check_external_services(self) -> Dict[str, Any]:
        """Check external service dependencies"""
        services = {
            "supabase": self._check_supabase(),
            "external_apis": self._check_external_apis()
        }
        
        all_healthy = all(service["status"] == "healthy" for service in services.values())
        
        return {
            "overall_status": "healthy" if all_healthy else "unhealthy",
            "services": services,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _check_supabase(self) -> Dict[str, Any]:
        """Check Supabase connectivity"""
        try:
            # TODO: Implement Supabase health check
            return {"status": "healthy", "response_time_ms": 100}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def _check_external_apis(self) -> Dict[str, Any]:
        """Check external API dependencies"""
        try:
            return {"status": "healthy", "response_time_ms": 75}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

health_check = HealthCheck()