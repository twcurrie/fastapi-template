import sentry_sdk

from typing import Any

from app import __version__
from app.core.config import settings


def delete_key(dict_: dict, key: Any):
    try:
        del dict_[key]
    except KeyError:
        pass


def before_send(event: dict, hint: dict):
    exceptions = event.get("exception")
    if not exceptions:
        return event

    for value in exceptions.get("values"):
        stacktrace = value.get("stacktrace")
        if not stacktrace:
            continue
        frames = stacktrace.get("frames") or []
        for frame in frames:
            """
            Within the fastapi library, `body` and `body_bytes` are captured
            in the exception during the request -> response processing for all
            endpoint functions.  This drops those values from the sentry event.
            Ref: https://github.com/tiangolo/fastapi/blob/master/fastapi/routing.py#L175-L197
            """
            if frame["module"] == "fastapi.routing":
                if frame["vars"]:
                    [delete_key(frame["vars"], key) for key in ["body", "body_bytes"]]
            """
            Within the httpx library, potentially PHI-containing fields 
            are captured in the exception during the actual HTTP request.
            This drops those values from the sentry event.
            Ref: https://github.com/encode/httpx/blob/master/httpx/_client.py#L1083-L1097
            """
            if frame["module"] == "httpx._client":
                if frame["vars"]:
                    [
                        delete_key(frame["vars"], key)
                        for key in [
                            "content",
                            "cookies",
                            "data",
                            "files",
                            "headers",
                            "json",
                            "params",
                        ]
                    ]
            """
            Within the SQLAlchemy library, `parameters` are captured in the exception 
            during the database transaction.  This drops those values from the sentry event.
            Ref: https://github.com/******
            """
            if (
                "sqlalchemy.engine" in frame["module"]
                or "sqlalchemy.sql" in frame["module"]
            ):
                if frame["vars"]:
                    """
                    These variables are parameters that have been unpacked in order
                    to be passed into a function and are captured in a viewable way,
                    so they must be dropped.
                    """
                    [
                        delete_key(frame["vars"], key)
                        for key in [
                            "args",
                            "args_10style",
                            "distilled_params",
                            "event_params",
                            "multiparams",
                        ]
                    ]
                if frame["module"] == "sqlalchemy.engine.base":
                    if frame["vars"]:
                        """
                        The PHI-hiding types handle all references to 'parameters' within
                        the library, except those within this module that have been unpacked.
                        """
                        delete_key(frame["vars"], "parameters")

    return event


sentry = sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT.value,
    before_send=before_send,
    release=__version__,
    traces_sample_rate=0.25,
)
