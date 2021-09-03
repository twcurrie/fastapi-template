import asyncio
from typing import Callable

import pytest
from mock import MagicMock
from sqlalchemy.orm import Session  # type: ignore
from starlette.testclient import TestClient

from app.api import deps
from app.main import app


@pytest.fixture(scope="function")
def mock_db() -> Session:
    return MagicMock()


@pytest.fixture(scope="function")
def get_mock_db(mock_db) -> Callable[[], Session]:
    return lambda: mock_db  # type: ignore


@pytest.fixture(scope="function")
def client(get_mock_db) -> TestClient:
    try:
        app.dependency_overrides[deps.get_db] = get_mock_db
    except AttributeError:
        # By using Sentry middleware, it wraps the app object requiring the
        # actual app be accessed through an additional object also called app.
        app.app.dependency_overrides[deps.get_db] = get_mock_db  # type: ignore
    return TestClient(app)


@pytest.fixture(scope="function")
def mock_example_api(mocker):
    future = asyncio.Future()
    future.set_result(["All good!"])
    mocker.patch("app.domain.example_api.get_status_checks", return_value=future)


@pytest.fixture(scope="function")
def failing_mock_example_api(mocker, side_effect):
    mocker.patch("app.domain.example_api.get_status_checks", side_effect=side_effect)
