"""
Logging configuration for La Vida Luca backend.
Provides structured JSON logging for production environments.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any
import sys

class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, "extra"):
            log_obj.update(record.extra)
            
        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_obj)

def setup_logging(service_name: str = "la-vida-luca-backend") -> logging.Logger:
    """
    Setup structured logging for the application.
    
    Args:
        service_name: Name of the service for log identification
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(service_name)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    
    # Add handler to logger
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger

class ContextLogger:
    """Logger with context management for request tracking."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.context: Dict[str, Any] = {}
        
    def set_context(self, **kwargs):
        """Set context variables for all subsequent log messages."""
        self.context.update(kwargs)
        
    def clear_context(self):
        """Clear all context variables."""
        self.context.clear()
        
    def _log_with_context(self, level: str, message: str, **kwargs):
        """Log message with current context."""
        extra = {**self.context, **kwargs}
        getattr(self.logger, level)(message, extra=extra)
        
    def debug(self, message: str, **kwargs):
        self._log_with_context("debug", message, **kwargs)
        
    def info(self, message: str, **kwargs):
        self._log_with_context("info", message, **kwargs)
        
    def warning(self, message: str, **kwargs):
        self._log_with_context("warning", message, **kwargs)
        
    def error(self, message: str, **kwargs):
        self._log_with_context("error", message, **kwargs)
        
    def critical(self, message: str, **kwargs):
        self._log_with_context("critical", message, **kwargs)

# Global logger instance
app_logger = setup_logging()
context_logger = ContextLogger(app_logger)