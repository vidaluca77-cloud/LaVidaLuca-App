"""Base database model and imports."""

# Import all models here to ensure they are known to SQLAlchemy
from .session import Base  # noqa
from ..models.user import User  # noqa
from ..models.location import Location  # noqa
from ..models.activity import Activity  # noqa
from ..models.booking import Booking  # noqa
from ..models.progress import Progress  # noqa
from ..models.message import Message  # noqa