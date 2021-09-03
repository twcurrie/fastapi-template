import logging

from app import __version__


class ContextProvidingLogFilter(logging.Filter):
    def __init__(self, **kwargs):
        self.extras = kwargs

        if __version__:
            # Provide app version within log JSON.
            self.extras["app.version"] = __version__
        super().__init__()

    def filter(self, record: logging.LogRecord) -> bool:
        if self.extras:
            for key, value in self.extras.items():
                record.__setattr__(key, value)
        return True
