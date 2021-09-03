import json
import logging

from app.core.logging.log import Log


class JsonLogFormatter(logging.Formatter):
    """The json log formatter converts LogRecord instances to strings via the
    format method.
    The json log format allows for arbitrary key/value pairs to be logged.
    This formatter automatically extracts all relevant information from the
    LogRecord (including extras) and places those key/values into a JSON
    object.
    Since the format is not configurable, all formatter constructor arguments
    are ignored.
    Usage::
        >>> import logging
        >>> record = logging.makeLogRecord({})
        >>> formatter = JsonLogFormatter()
        >>> result = formatter.format(record)
        >>> isinstance(result, str)
        True
    """

    def __init__(self, *args, **kwargs):
        super(JsonLogFormatter, self).__init__()

    def format(self, record):
        """Format the specified record as text
        :param record: The LogRecord to format.
        :type record: logging.LogRecord
        :rtype: str
        """
        return json.dumps(Log.extract_record_data(record), separators=(",", ":"))
