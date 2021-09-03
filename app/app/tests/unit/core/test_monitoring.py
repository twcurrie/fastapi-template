from pydantic import BaseModel

import json

from app.core.monitoring import contains_phi
from app.core.monitoring.sentry import before_send


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
            if isinstance(parent, dict) and "newrelic.hooks.database" in parent.get(
                "module", ""
            ):
                assert "args" not in obj_
            for value in obj_.values():
                dict_checker(obj_, value)
        elif isinstance(obj_, list) or isinstance(obj_, tuple):
            for v in obj_:
                dict_checker(obj_, v)
        else:
            pass

    dict_checker(None, processed_event)
