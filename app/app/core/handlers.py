"""
These handlers translate custom exceptions into HTTP responses.
"""


from fastapi.encoders import jsonable_encoder
from sentry_sdk import capture_exception
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.exceptions import (
    ApiSerializationError,
    ApiTimeoutError,
)
from app.core.logging import get_logger


def rate_limiter_exception_handler(request: Request, exc: RateLimitExceeded):
    logger = get_logger(name=__name__)
    logger.warning(*exc.args, extra={"request.id": request.state.id})
    capture_exception(exc)
    response = JSONResponse(
        status_code=429,
        content=jsonable_encoder({"message": f"Rate limit exceeded ({exc.detail})."}),
    )
    return response


def api_serialization_exception_handler(request: Request, exc: ApiSerializationError):
    logger = get_logger(name=__name__)
    logger.warning(
        *exc.args,
        extra={"request.id": request.state.id, "provider.endpoint": exc.api_endpoint},
    )
    capture_exception(exc)
    response = JSONResponse(
        status_code=424,
        content=jsonable_encoder(
            {"message": "Response from supporting API can not be parsed."}
        ),
    )
    return response


def api_timeout_exception_handler(request: Request, exc: ApiTimeoutError):
    logger = get_logger(name=__name__)
    logger.warning(
        *exc.args,
        extra={"request.id": request.state.id, "provider.endpoint": exc.api_endpoint},
    )
    capture_exception(exc)
    response = JSONResponse(
        status_code=504,
        content=jsonable_encoder({"message": "Supporting API is not available."}),
    )
    return response
