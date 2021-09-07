import logging
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from app.core.middleware.http import RequestLoggingMiddleware, RequestTimingMiddleware


logging_app = Starlette()
logging_app.add_middleware(RequestLoggingMiddleware)


@logging_app.route("/")
def logging_homepage(request):
    return PlainTextResponse("Homepage")


def test__request_logging_middleware(caplog):
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    client = TestClient(logging_app)
    response = client.get("/")

    assert "X-Request-Id" in response.headers
    request_id = response.headers["X-Request-Id"]
    assert all(
        [
            request_id in record.message
            for record in caplog.records
            if record.levelname == "INFO"
        ]
    )


timing_app = Starlette()
timing_app.add_middleware(RequestTimingMiddleware)


@timing_app.route("/")
def timing_homepage(request):
    return PlainTextResponse("Homepage")


def test__request_timing_middleware(caplog):
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    client = TestClient(timing_app)
    response = client.get("/")

    assert "X-Process-Time" in response.headers
