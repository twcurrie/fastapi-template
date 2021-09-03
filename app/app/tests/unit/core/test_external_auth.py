import pytest
import hiro  # type: ignore
from pytest_httpx import HTTPXMock  # type: ignore
from freezegun import freeze_time

import asyncio
from datetime import timedelta
from pydantic import ValidationError

from app.core.external_auth import BaseCredentials, BaseOAuthResponse, BaseOAuthRequest
from app.core.exceptions import ApiAuthenticationError


@pytest.fixture(autouse=True)
def clean_up_credentials():
    ConcreteBaseCredentials._reset()  # noqa


class ConcreteBaseCredentials(BaseCredentials[BaseOAuthRequest, BaseOAuthResponse]):
    @property
    def authentication_endpoint(self) -> str:
        return "http://localhost:8080/not/an/actual/auth"

    @property
    def authentication_request(self) -> BaseOAuthRequest:
        return BaseOAuthRequest(client_id="not_an_id", client_secret="not_a_secret")


@pytest.mark.asyncio
async def test__singleton__multiple_threads():
    threads = 10

    def get_credentials() -> BaseCredentials:
        return ConcreteBaseCredentials(
            BaseOAuthRequest,
            BaseOAuthResponse,
            oauth_response=BaseOAuthResponse(access_token="token", expires_in=threads),
        )

    credentials = get_credentials()

    async def compare_object():
        credentials_in_thread = get_credentials()
        # All objects created are in fact the same:
        assert credentials == credentials_in_thread

    await asyncio.gather(
        *[compare_object() for _ in range(threads)], return_exceptions=False
    )


@freeze_time("Jan 14th, 2020", auto_tick_seconds=3)
def test__expired__true():
    credentials = ConcreteBaseCredentials(
        BaseOAuthRequest,
        BaseOAuthResponse,
        oauth_response=BaseOAuthResponse(access_token="token", expires_in=2),
    )
    assert credentials.expired is True


@freeze_time("Jan 14th, 2020", auto_tick_seconds=1)
def test__expired__false():
    credentials = ConcreteBaseCredentials(
        BaseOAuthRequest,
        BaseOAuthResponse,
        oauth_response=BaseOAuthResponse(access_token="token", expires_in=2),
    )
    assert credentials.expired is False


def test__retrieve_token__success(httpx_mock: HTTPXMock):
    example_token = "this is the token"
    httpx_mock.add_response(
        status_code=200,
        json=BaseOAuthResponse(
            access_token=example_token, token_type="bearer", expires_in=300
        ).dict(),
    )
    credentials = ConcreteBaseCredentials(BaseOAuthRequest, BaseOAuthResponse)

    assert (
        credentials.authorization_header["Authorization"] == f"Bearer {example_token}"
    )


def test__retrieve_token__validation_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=200, json={"this_is": "not_the_content"})
    credentials = ConcreteBaseCredentials(BaseOAuthRequest, BaseOAuthResponse)
    with pytest.raises(ValidationError):
        credentials.retrieve_token()


def test__retrieve_token__error_with_json(httpx_mock: HTTPXMock):
    message = "an important error message"
    httpx_mock.add_response(status_code=403, json={"a_key": message})
    credentials = ConcreteBaseCredentials(BaseOAuthRequest, BaseOAuthResponse)
    with pytest.raises(ApiAuthenticationError) as e:
        credentials.retrieve_token()
    assert message in str(e)


def test__retrieve_token__error_no_json(httpx_mock: HTTPXMock):
    message = "an important error message"
    httpx_mock.add_response(status_code=403, json={"error": message})
    credentials = ConcreteBaseCredentials(BaseOAuthRequest, BaseOAuthResponse)
    with pytest.raises(ApiAuthenticationError) as e:
        credentials.retrieve_token()
    assert message in str(e)


def test__refresh_token__token_refreshed_on_access(httpx_mock: HTTPXMock):
    refreshed_token = "this is the token"
    httpx_mock.add_response(
        status_code=200,
        json=BaseOAuthResponse(
            access_token=refreshed_token, token_type="bearer", expires_in=1
        ).dict(),
    )

    with hiro.Timeline() as timeline:
        expired_token = "this was the token"
        credentials = ConcreteBaseCredentials(
            BaseOAuthRequest,
            BaseOAuthResponse,
            oauth_response=BaseOAuthResponse(access_token=expired_token, expires_in=1),
        )
        timeline.freeze()
        assert (
            credentials.authorization_header["Authorization"]
            == f"Bearer {expired_token}"
        )
        timeline.forward(timedelta(seconds=1))

        timeline.freeze()
        assert (
            credentials.authorization_header["Authorization"]
            == f"Bearer {refreshed_token}"
        )
