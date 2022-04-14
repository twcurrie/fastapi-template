import pytest
from pytest_httpx import HTTPXMock  # type: ignore

import httpx

from app.domain import example_api
from app.core.exceptions import ApiSerializationError, ApiTimeoutError
from app.schemas.external.example_api import StatusCheck
from app.core.config import settings


@pytest.mark.asyncio
async def test__request_status_check__validation_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=200, json={"content": "not_correct"})

    async with httpx.AsyncClient() as client:
        with pytest.raises(ApiSerializationError) as e:
            await example_api.request_status_check(client)
    assert settings.EXAMPLE_API_ENDPOINT in str(e.value)


@pytest.mark.asyncio
async def test__request_status_check__timeout_error(httpx_mock: HTTPXMock):
    def raise_timeout(request: httpx.Request):
        raise httpx.ReadTimeout(f"Unable to read within timeout", request=request)

    httpx_mock.add_callback(raise_timeout)
    async with httpx.AsyncClient() as client:
        with pytest.raises(ApiTimeoutError) as e:
            await example_api.request_status_check(client)
    assert settings.EXAMPLE_API_ENDPOINT in str(e.value)


@pytest.mark.asyncio
async def test__request_status_check__success(httpx_mock: HTTPXMock):
    expected_message = "It's just fine."
    httpx_mock.add_response(status_code=200, json={"value": expected_message})

    async with httpx.AsyncClient() as client:
        response = await example_api.request_status_check(client)
    assert response.value == expected_message


@pytest.mark.asyncio
async def test__get_status_checks__total_failure(mocker):
    number_of_checks = 3
    side_effects = number_of_checks * [ApiTimeoutError]
    mocker.patch(
        "app.domain.example_api.request_status_check",
        side_effect=side_effects,
    )

    with pytest.raises(ApiTimeoutError):
        await example_api.get_status_checks(number_of_checks)


@pytest.mark.asyncio
async def test__get_status_checks__partial_failure(mocker):
    number_of_checks = 3
    expected_message = "My friend isn't well!"

    future_status = StatusCheck(value=expected_message)
    mocker.patch(
        "app.domain.example_api.request_status_check",
        side_effect=(number_of_checks - 1) * [future_status] + [ApiTimeoutError],
    )
    status_checks = await example_api.get_status_checks(number_of_checks - 1)
    assert all([status == expected_message for status in status_checks])

    with pytest.raises(ApiTimeoutError):
        await example_api.get_status_checks(1)


@pytest.mark.asyncio
async def test__get_status_checks__success(mocker):
    number_of_checks = 3
    expected_message = "Thanks for checking on me."
    mocker.patch(
        "app.domain.example_api.request_status_check",
        return_value=StatusCheck(value=expected_message),
    )

    status_checks = await example_api.get_status_checks(number_of_checks)
    assert all([status == expected_message for status in status_checks])
