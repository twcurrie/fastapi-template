from .formatter import JsonLogFormatter
from .filter import ContextProvidingLogFilter


def get_logger(name: str, **kwargs):
    import logging

    logger = logging.getLogger(name)
    logger.addFilter(ContextProvidingLogFilter(**kwargs))
    return logger
