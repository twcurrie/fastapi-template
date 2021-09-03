LOGGING_CONFIG = {
    "version": 1,
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": [
                "custom_handler",
            ],
        },
        "gunicorn": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
    },
    "handlers": {
        "custom_handler": {
            "level": "DEBUG",
            "formatter": "custom_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": ["custom_filter"],
        },
    },
    "filters": {
        "custom_filter": {
            "()": "app.core.logging.ContextProvidingLogFilter",
        },
    },
    "formatters": {"custom_formatter": {"()": "app.core.logging.JsonLogFormatter"}},
}
