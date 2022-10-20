import os
from datetime import datetime
from typing import List, Dict, Any

from datadog import initialize, api
from ddtrace.ext import aws

from app import __version__  # noqa

DEFAULT_TAGS = [
    f"version:{__version__}",
    f"env:{os.environ.get('DD_ENV')}",
    "service:eligibility-service",
]

options: Dict[str, Any] = {}

initialize(**options)

# To emit custom metrics from the application, do the following
#
# from app.core.monitoring.datadog import datadog_metric
#
# datadog_metric(payload={"exception": 1}, tags=["status_code:424"])
def datadog_metric(payload: Dict[str, int], tags: List[str] = []) -> None:
    BASE_KEY = "eligibility-service"

    for k, v in payload.items():
        api.Metric.send(
            metric=f"{BASE_KEY}.{k}",
            points=(datetime.timestamp(datetime.now()), v),
            tags=[*DEFAULT_TAGS, *tags],
        )


def datadog_event(title: str, text: str, alert_type: str, tags: List[str]) -> None:
    api.Event.create(
        **{
            "title": title,
            "text": text,
            "alert_type": alert_type,
            "tags": [*DEFAULT_TAGS, *tags],
        }
    )


# NOTE: EXCLUDED_ENDPOINT_TAGS is an internal constant to the ddtrace library,
# this hack may break in future versions of ddtrace but should be caught by our unit test
def exclude_aws_endpoint_tag(endpoint: str, tags: set):
    excluded_endpoint_tags = aws.EXCLUDED_ENDPOINT_TAGS
    excluded_endpoint_tags[endpoint] = frozenset(tags)
    aws.EXCLUDED_ENDPOINT_TAGS = excluded_endpoint_tags


# params.QueryString contains PHI in athena queries, so we do not want to send this tag to DD
exclude_aws_endpoint_tag("athena", {"params.QueryString"})
