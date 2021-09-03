import pytest

from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasicCredentials

from app.core.security import authenticate_http_basic


def test__authenticate_http_basic__returns_true():
    credentials = HTTPBasicCredentials(username="hingehealth", password="swordfish")

    assert authenticate_http_basic(credentials) == True


def test__authenticate_http_basic_raises_on_fail():
    credentials = HTTPBasicCredentials(username="foo", password="bar")

    with pytest.raises(HTTPException):
        assert authenticate_http_basic(credentials)
