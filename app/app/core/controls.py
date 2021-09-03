from slowapi.extension import Limiter
from slowapi.util import get_ipaddr

from app.core.config import settings

rate_limiter = Limiter(
    key_func=get_ipaddr,
    default_limits=[],  # Example value of "1/minute"
    application_limits=[],
    strategy="fixed-window",
    storage_uri=settings.REDIS_URI,
    enabled=settings.ENABLE_RATE_LIMITING,
)
