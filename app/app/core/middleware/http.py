import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
    Response,
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    TARGET_REQUEST_PROPERTIES = [
        "type",
        "http_version",
        "server",
        "client",
        "scheme",
        "method",
        "path",
        "query_string",
    ]

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = uuid4()
        request.state.id = request_id
        extras = {
            f"request.{k}": v
            for k, v in request.scope.items()
            if k in self.TARGET_REQUEST_PROPERTIES
        }

        logging.info(
            f"Processing request id: {request_id}",
            extra={"request.id": request_id, **extras},
        )
        response = await call_next(request)
        logging.info(
            f"Sending response to request id: {request_id}.",
            extra={
                "request.id": request_id,
                "response.status_code": response.status_code,
                **extras,
            },
        )
        response.headers["X-Request-Id"] = str(request_id)
        return response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
