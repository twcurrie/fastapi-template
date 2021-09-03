import json
import logging
import os
import sys
import threading
from freezegun import freeze_time

import pytest

from app.core.logging.formatter import JsonLogFormatter
from app.core.logging.log import Log, extract_from_tuple


class MyError(Exception):
    pass


BASE_RECORD_DICT = {
    "name": "test_record",
    "levelname": "WARNING",
    "pathname": "/",
    "lineno": 12,
    "msg": "message",
}


@pytest.mark.parametrize("extras", ({}, {"extra": "a little bit"}))
def test__log__extract_data_success(extras):
    record_dict = BASE_RECORD_DICT.copy()
    record_dict.update(extras)
    record = logging.makeLogRecord(record_dict)
    output = Log.extract_record_data(record)
    current_thread = threading.current_thread()
    expected_output = {
        "timestamp": int(record.created * 1000),
        "message": "message",
        "log.level": "WARNING",
        "logging.name": "test_record",
        "thread.id": current_thread.ident,
        "thread.name": current_thread.name,
        "process.id": os.getpid(),
        "process.name": "MainProcess",
        "file.name": "/",
        "line.number": 12,
    }
    expected_output.update(extras)
    assert output == expected_output


@pytest.mark.parametrize(
    "error_cls",
    (ValueError, MyError),
)
def test__log__extract_data_exception(error_cls):
    try:
        raise error_cls("uh oh")
    except Exception:
        exc_info = sys.exc_info()
    record = logging.makeLogRecord({"exc_info": exc_info})

    # Log is instantiated here to ensure a staticmethod is used
    output = Log("").extract_record_data(record)

    cls_name = ".".join((error_cls.__module__, error_cls.__name__))

    assert output["error.class"] == cls_name
    assert output["error.message"] == "uh oh"
    assert 'raise error_cls("uh oh")\n' in output["error.stack"]


@pytest.mark.parametrize(
    "attributes",
    (
        {},
        {"foo": "bar"},
    ),
)
def test__log__successful_creation(attributes):
    log = Log("message", timestamp=1, **attributes)
    expected = {
        "timestamp": 1,
        "message": "message",
    }
    if attributes:
        expected["attributes"] = attributes
    assert dict(log) == expected


@freeze_time("January 1st, 2000")
def test__log__default_timestamp():
    log = Log("message")
    assert dict(log) == {
        "message": "message",
        "timestamp": 946684800000,  # Timestamp for Y2K
    }


def test__log__from_log_record():
    record = logging.makeLogRecord(
        {
            "name": "test_record",
            "levelname": "WARNING",
            "pathname": "/",
            "lineno": 12,
            "msg": "Logger exception",
            "extra_str": "str",
            "extra_int": 9000,
            "extra_float": 1.23,
            "extra_bool": True,
            "extra_dict": {},
            "extra_tuple": (),
            "extra_list": [],
        }
    )
    log = Log.from_record(record)

    current_thread = threading.current_thread()
    assert dict(log) == {
        "timestamp": int(record.created * 1000),
        "message": "Logger exception",
        "attributes": {
            "log.level": "WARNING",
            "logging.name": "test_record",
            "thread.id": current_thread.ident,
            "thread.name": current_thread.name,
            "process.id": os.getpid(),
            "process.name": "MainProcess",
            "file.name": "/",
            "line.number": 12,
            "extra_str": "str",
            "extra_int": 9000,
            "extra_float": 1.23,
            "extra_bool": True,
            "extra_dict": "{}",
            "extra_tuple": "()",
            "extra_list": "[]",
        },
    }


@pytest.mark.parametrize("extras", ({}, {"extra": "yes"}))
def test__log__formatted_json(extras):
    # Verify specifying arguments do not crash
    formatter = JsonLogFormatter("%(message)s", datefmt="%Y")
    record_dict = BASE_RECORD_DICT.copy()
    record_dict.update(extras)
    record = logging.makeLogRecord(record_dict)
    output = formatter.format(record)

    # Verify all spaces have been removed
    assert " " not in output

    # Output is valid JSON
    current_thread = threading.current_thread()
    expected_output = {
        "timestamp": int(record.created * 1000),
        "message": "message",
        "log.level": "WARNING",
        "logging.name": "test_record",
        "thread.id": current_thread.ident,
        "thread.name": current_thread.name,
        "process.id": os.getpid(),
        "process.name": "MainProcess",
        "file.name": "/",
        "line.number": 12,
    }
    expected_output.update(extras)
    assert json.loads(output) == expected_output


def test__extract_from_tuple__success():
    result = extract_from_tuple(
        ("2", 3, "another_value"), mapping={0: "a string", 1: "an int"}
    )
    expected = {"a string": "2", "an int": 3}
    assert expected == result


def test__extract_from_tuple__no_value_present():
    result = extract_from_tuple(
        ("2", 3, "another_value"), mapping={1: "an int", 5: "not there :-("}
    )
    expected = {"an int": 3}
    assert expected == result
