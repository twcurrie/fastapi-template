from typing import Generator

import pytest
from mock import MagicMock, Mock, AsyncMock

from app.core.health.checks import is_database_available, is_redis_available


@pytest.fixture(scope="function")
def session(side_effect):
    mock_session = MagicMock()
    mock_session.execute = Mock(side_effect=side_effect)
    yield mock_session


@pytest.fixture(scope="function")
def async_session(return_value) -> Generator:
    mock_session = AsyncMock()
    mock_session.ping = AsyncMock(return_value=return_value)
    yield mock_session


@pytest.fixture(scope="function")
def async_session_with_side_effect(side_effect) -> Generator:
    mock_session = AsyncMock()
    mock_session.ping = AsyncMock(side_effect=side_effect)
    yield mock_session


@pytest.mark.parametrize(
    "side_effect, expected_value",
    [(None, True), (Exception, False)],
)
def test__database__health(session, expected_value: bool):
    assert is_database_available(session) == expected_value


@pytest.mark.asyncio
@pytest.mark.parametrize("return_value", [b"PONG"])
async def test__redis__health(async_session):
    assert await is_redis_available(async_session)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "side_effect",
    [Exception],
)
async def test__redis__health__exception(async_session_with_side_effect):
    assert not await is_redis_available(async_session_with_side_effect)
