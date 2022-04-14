import pytest
from pydantic import BaseModel

import json
import logging
from typing import Any

from app.core.monitoring import contains_phi, handles_phi
from app.core.monitoring.sentry import before_send


@pytest.mark.parametrize("sensitive_data", ["Jane Doe", 123, 1.0])
def test__handles_phi__exception_success(sensitive_data):
    @handles_phi
    def method_handling_phi_primitives(a_sensitive_field: Any) -> None:
        raise ValueError(a_sensitive_field)

    with pytest.raises(ValueError) as e:
        method_handling_phi_primitives(sensitive_data)

    assert str(sensitive_data) not in str(e.value.args[0])


@pytest.mark.parametrize("sensitive_data", ["Jane Doe", 123, 1.0])
def test__handles_phi__logging_success(caplog, sensitive_data):
    @handles_phi
    def method_handling_phi_primitives(a_sensitive_field: Any) -> None:
        logging.info(f"A sensitive field is being processed: {a_sensitive_field}")
        assert a_sensitive_field.has_phi  # type: ignore

    caplog.clear()
    caplog.set_level(logging.INFO)

    method_handling_phi_primitives(sensitive_data)
    assert sensitive_data not in [record.message for record in caplog.records]


@pytest.mark.parametrize("sensitive_data", ["Jane Doe", 123, 1.0])
def test__handles_phi__sub_function_success(caplog, sensitive_data):
    def method_unknowingly_handling_phi_primitives(maybe_sensitive_field: Any) -> None:
        logging.info(
            f"We might be processing a sensitive field: {maybe_sensitive_field}"
        )
        assert maybe_sensitive_field.has_phi  # type: ignore

    @handles_phi
    def method_handling_phi_primitives(a_sensitive_field: Any) -> None:
        method_unknowingly_handling_phi_primitives(a_sensitive_field)

    caplog.clear()
    caplog.set_level(logging.INFO)

    method_handling_phi_primitives(sensitive_data)
    assert sensitive_data not in [record.message for record in caplog.records]


@pytest.mark.parametrize("sensitive_data", ["Jane Doe", 123, 1.0])
def test__handles_phi_with_args__exception_success(sensitive_data):
    @handles_phi(sensitive_fields=["a_sensitive_field"])
    def method_handling_phi_primitives(a_sensitive_field: Any, a_field: str) -> None:
        raise ValueError(f"{a_sensitive_field} - {a_field}")

    insensitive_data = "bull-in-a-china shop"
    with pytest.raises(ValueError) as e:
        method_handling_phi_primitives(sensitive_data, insensitive_data)

    assert str(sensitive_data) not in str(e.value.args[0])
    assert insensitive_data in str(e.value.args[0])


@pytest.mark.parametrize("sensitive_data", ["Jane Doe", 123, 1.0])
def test__handles_phi_with_args__logging_success(caplog, sensitive_data):
    @handles_phi(sensitive_fields=["a_sensitive_field"])
    def method_handling_phi_primitives(a_sensitive_field: Any, a_field: str) -> None:
        logging.info(f"A sensitive field is being processed: {a_sensitive_field}")
        assert a_sensitive_field.has_phi  # type: ignore

    caplog.clear()
    caplog.set_level(logging.INFO)

    insensitive_data = "feelings"
    method_handling_phi_primitives(sensitive_data, insensitive_data)
    assert sensitive_data not in [record.message for record in caplog.records]


@pytest.mark.parametrize("sensitive_data", ["Jane Doe", 123, 1.0])
def test__handles_phi_with_args__sub_function_success(caplog, sensitive_data):
    def method_unknowingly_handling_phi_primitives(
            maybe_sensitive_field: Any, a_field: Any
    ) -> None:
        logging.info(
            f"We might be processing a sensitive fields: {maybe_sensitive_field}, {a_field}"
        )
        assert maybe_sensitive_field.has_phi  # type: ignore

    @handles_phi(sensitive_fields=["a_sensitive_field"])
    def method_handling_phi_primitives(a_sensitive_field: Any, a_field: str) -> None:
        method_unknowingly_handling_phi_primitives(a_sensitive_field, a_field)

    caplog.clear()
    caplog.set_level(logging.INFO)

    insensitive_data = "just-no-remorse"
    method_handling_phi_primitives(sensitive_data, insensitive_data)
    assert sensitive_data not in [record.message for record in caplog.records]


@pytest.mark.parametrize("sensitive_data", ["Jane Doe", 123, 1.0])
def test__handles_phi_with_kwargs__exception_success(sensitive_data):
    @handles_phi(sensitive_fields=["a_sensitive_field"])
    def method_handling_phi_primitives(a_sensitive_field: Any, a_field: str) -> None:
        raise ValueError(f"{a_sensitive_field} - {a_field}")

    insensitive_data = "bull-in-a-china shop"
    with pytest.raises(ValueError) as e:
        method_handling_phi_primitives(
            a_sensitive_field=sensitive_data, a_field=insensitive_data
        )

    assert str(sensitive_data) not in str(e.value.args[0])
    assert insensitive_data in str(e.value.args[0])


@pytest.mark.parametrize("sensitive_data", ["Jane Doe", 123, 1.0])
def test__handles_phi_with_kwargs__logging_success(caplog, sensitive_data):
    @handles_phi(sensitive_fields=["a_sensitive_field"])
    def method_handling_phi_primitives(a_sensitive_field: Any, a_field: str) -> None:
        logging.info(f"A sensitive field is being processed: {a_sensitive_field}")
        assert a_sensitive_field.has_phi  # type: ignore

    caplog.clear()
    caplog.set_level(logging.INFO)

    insensitive_data = "feelings"
    method_handling_phi_primitives(
        a_sensitive_field=sensitive_data, a_field=insensitive_data
    )
    assert sensitive_data not in [record.message for record in caplog.records]


@pytest.mark.parametrize("sensitive_data", ["Jane Doe", 123, 1.0])
def test__handles_phi_with_kwargs__sub_function_success(caplog, sensitive_data):
    def method_unknowingly_handling_phi_primitives(
            maybe_sensitive_field: Any, a_field: Any
    ) -> None:
        logging.info(
            f"We might be processing a sensitive fields: {maybe_sensitive_field}, {a_field}"
        )
        assert maybe_sensitive_field.has_phi  # type: ignore

    @handles_phi(sensitive_fields=["a_sensitive_field"])
    def method_handling_phi_primitives(a_sensitive_field: Any, a_field: str) -> None:
        method_unknowingly_handling_phi_primitives(a_sensitive_field, a_field)

    caplog.clear()
    caplog.set_level(logging.INFO)

    insensitive_data = "just-no-remorse"
    method_handling_phi_primitives(
        a_sensitive_field=sensitive_data, a_field=insensitive_data
    )
    assert sensitive_data not in [record.message for record in caplog.records]


def test__contains_phi__success():
    class ContainsPHI(BaseModel):
        social_security_number: int

    @contains_phi
    class SanitizedPHI(ContainsPHI):
        pass

    class StillNotExposedPHI(SanitizedPHI):
        pass

    ssn = 1111111111
    phi = ContainsPHI(social_security_number=ssn)
    sanitized_phi = SanitizedPHI(social_security_number=ssn)
    still_not_exposed_phi = StillNotExposedPHI(social_security_number=ssn)

    assert str(ssn) in phi.__repr__()
    assert str(ssn) not in sanitized_phi.__repr__()
    assert str(ssn) not in still_not_exposed_phi.__repr__()


def test__before_send__sanitizes_requests__fastapi(get_resource):
    with get_resource("sentry_exception__fastapi__with_phi.json") as json_with_phi:
        event_with_phi = json.load(json_with_phi)

    processed_event = before_send(event_with_phi, {})

    def dict_checker(obj_):
        """
        Recursively checks dictionary for `body` and `body_bytes`
        """
        if isinstance(obj_, dict):
            assert "body" not in obj_
            assert "body_bytes" not in obj_
            for value in obj_.values():
                dict_checker(value)
        elif isinstance(obj_, list) or isinstance(obj_, tuple):
            for v in obj_:
                dict_checker(v)
        else:
            pass

    dict_checker(processed_event)


def test__before_send__sanitizes_requests__httpx(get_resource):
    with get_resource("sentry_exception__httpx__with_phi.json") as json_with_phi:
        event_with_phi = json.load(json_with_phi)

    processed_event = before_send(event_with_phi, {})

    def dict_checker(parent, obj_):
        """
        Recursively checks dictionary for http request parameters included from httpx
        """
        if isinstance(obj_, dict):
            if isinstance(parent, dict) and parent.get("module") == "httpx._client":
                assert "headers" not in obj_
                assert "data" not in obj_
                assert "params" not in obj_
                assert "content" not in obj_
                assert "json" not in obj_
                assert "cookies" not in obj_
                assert "files" not in obj_
            for value in obj_.values():
                dict_checker(obj_, value)
        elif isinstance(obj_, list) or isinstance(obj_, tuple):
            for v in obj_:
                dict_checker(obj_, v)
        else:
            pass

    dict_checker(None, processed_event)


def test__before_send__sanitizes_requests__sqlalchemy(get_resource):
    with get_resource("sentry_exception__sqlalchemy__with_phi.json") as json_with_phi:
        event_with_phi = json.load(json_with_phi)

    processed_event = before_send(event_with_phi, {})

    def dict_checker(parent, obj_):
        """
        Recursively checks dictionary for http request parameters included from httpx
        """
        if isinstance(obj_, dict):
            if (
                    isinstance(parent, dict)
                    and parent.get("module") == "sqlalchemy.engine.base"
            ):
                assert "parameters" not in obj_
            if isinstance(parent, dict) and "sqlalchemy.engine" in parent.get(
                    "module", ""
            ):
                assert "args" not in obj_
                assert "args_10style" not in obj_
                assert "distilled_params" not in obj_
                assert "event_params" not in obj_
            if isinstance(parent, dict) and "sqlalchemy.sql" in parent.get(
                    "module", ""
            ):
                assert "multiparams" not in obj_
            for value in obj_.values():
                dict_checker(obj_, value)
        elif isinstance(obj_, list) or isinstance(obj_, tuple):
            for v in obj_:
                dict_checker(obj_, v)
        else:
            pass

    dict_checker(None, processed_event)
