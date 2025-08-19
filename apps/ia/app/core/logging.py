import logging
import sys
from typing import Any
from .config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log") if settings.environment == "production" else logging.NullHandler(),
    ],
)

logger = logging.getLogger("lavidaluca-api")


def log_info(message: str, **kwargs: Any) -> None:
    """Log info message with optional context."""
    logger.info(message, extra=kwargs)


def log_error(message: str, **kwargs: Any) -> None:
    """Log error message with optional context."""
    logger.error(message, extra=kwargs)


def log_warning(message: str, **kwargs: Any) -> None:
    """Log warning message with optional context."""
    logger.warning(message, extra=kwargs)


def log_debug(message: str, **kwargs: Any) -> None:
    """Log debug message with optional context."""
    logger.debug(message, extra=kwargs)