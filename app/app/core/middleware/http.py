import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
    Response,
)

from app.core.monitoring.datadog import datadog_event


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

        # # issue fix: https://stackoverflow.com/questions/71222144/runtimeerror-no-response-returned-in-fastapi-when-refresh-request
        # # Workaround 2
        try:
            response = await call_next(request)
        except RuntimeError as exc:
            if await request.is_disconnected():
                datadog_event(
                    title="Client Disconnected before response",
                    text=str(exc),
                    alert_type="error",
                    tags=["status_code:204"],
                )
                return Response(status_code=204)
            raise

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
