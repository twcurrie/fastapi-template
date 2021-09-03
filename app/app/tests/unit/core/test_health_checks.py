import asyncio
from typing import Generator

import pytest
from mock import MagicMock, Mock

from app.core.health.checks import is_database_available, is_redis_available


@pytest.fixture(scope="function")
def session(side_effect):
    mock_session = MagicMock()
    mock_session.execute = Mock(side_effect=side_effect)
    yield mock_session


@pytest.fixture(scope="function")
def async_session(response) -> Generator:
    mock_session = MagicMock()
    future_status: asyncio.Future = asyncio.Future()
    future_status.set_result(response)
    mock_session.execute = Mock(return_value=future_status)
    yield mock_session


@pytest.mark.parametrize(
    "side_effect, expected_value",
    [(None, True), (Exception, False)],
)
def test__database__health(session, expected_value: bool):
    assert is_database_available(session) == expected_value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response, expected_value",
    [(b"PONG", True), (b"PING", False)],
)
async def test__redis__health(async_session, expected_value: bool):
    assert await is_redis_available(async_session) == expected_value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "side_effect, expected_value",
    [(Exception, False)],
)
async def test__redis__health__exception(session, expected_value: bool):
    assert await is_redis_available(session) == expected_value
