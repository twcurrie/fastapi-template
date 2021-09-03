# import asyncio
import logging
import time
from uuid import uuid4

# from aio_pika import connect_robust
# from aio_pika.patterns import RPC
from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
    Response,
)

# from app.core.config import settings


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


#
# async def rpc_middleware(request: Request, call_next):
#     try:
#         loop = asyncio.get_event_loop()
#         connection = await connect_robust(settings.AMQP_URI, loop=loop)
#         channel = await connection.channel()
#         request.state.rpc = await RPC.create(channel)
#         response = await call_next(request)
#     except:
#         response = Response("Internal server error", status_code=500)
#     finally:
#
#         # UPD: just thought that we probably want to keep queue and don't
#         # recreate it for each request so we can remove this line and move
#         # connection, channel and rpc initialisation out from middleware
#         # and do it once on app start
#
#         # Also based of this: https://github.com/encode/starlette/issues/1029
#         # it's better to create ASGI middleware instead of HTTP
#         await request.state.rpc.close()
#     return response
