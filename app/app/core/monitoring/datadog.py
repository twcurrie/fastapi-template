import os
from app import __version__
from datadog import initialize, statsd

options = {
    "statsd_host": os.environ.get("DD_TRACE_AGENT_HOST"),
    "statsd_port": 8125,
    "statsd_constant_tags": f"version:{__version__},env:{os.environ.get('DD_ENV')}",
}

initialize(**options)  # type: ignore


# To emit custom metrics or events from the application, do the following
#
# from app.core.monitoring.datadog import statsd
#
# statsd.increment("<metric-name>", tags=['env:dev'])
# (ref: https://docs.datadoghq.com/metrics/dogstatsd_metrics_submission/ )
#
# statsd.event('An error occurred', 'Error message', alert_type='error', tags=['env:dev'])
# (ref:  https://docs.datadoghq.com/events/guides/dogstatsd/ )
