from app.core.config import settings  # noqa

if (
    not settings.ENVIRONMENT.is_testing() and not settings.ENVIRONMENT.is_development()
):  # pragma: no cover
    # Disable new relic monitoring during testing and development
    from app.core.monitoring.new_relic import *  # noqa

import logging.config

from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v0.api import api_router as v0_router
from app.core import version
from app.core.controls import rate_limiter
from app.core.exceptions import (
    ApiSerializationError,
    ApiTimeoutError,
)
from app.core.handlers import (
    api_serialization_exception_handler,
    api_timeout_exception_handler,
    rate_limiter_exception_handler,
)
from app.core.health.checks import checks
from app.core.health import route
from app.core.logging.config import LOGGING_CONFIG
from app.core.logging.formatter import JsonLogFormatter
from app.core.middleware.http import RequestLoggingMiddleware, RequestTimingMiddleware
from app.core.monitoring import sentry

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V0_STR}/openapi.json",
    docs_url=None if settings.ENVIRONMENT.is_production() else "/docs",
    redoc_url=None if settings.ENVIRONMENT.is_production() else "/redoc",
)

app.include_router(v0_router, prefix=settings.API_V0_STR)
app.state.limiter = rate_limiter
app.state.monitor = sentry

app.add_exception_handler(ApiSerializationError, api_serialization_exception_handler)
app.add_exception_handler(ApiTimeoutError, api_timeout_exception_handler)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestTimingMiddleware)

if settings.ENABLE_RATE_LIMITING:  # pragma: no cover
    app.add_middleware(SlowAPIMiddleware)
    app.add_exception_handler(RateLimitExceeded, rate_limiter_exception_handler)
app.add_api_route("/health", rate_limiter.exempt(route.health(checks)))
app.add_api_route("/version", version.endpoint)


app = SentryAsgiMiddleware(app)  # type: ignore

handler = logging.StreamHandler()
handler.formatter = JsonLogFormatter()
logging.config.dictConfig(LOGGING_CONFIG)

# For local debugging of service.
if __name__ == "__main__":
    import uvicorn  # type: ignore

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)  # nosec
