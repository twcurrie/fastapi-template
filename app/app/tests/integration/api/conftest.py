import pytest
from sqlalchemy.orm import Session  # type: ignore
from starlette.testclient import TestClient

from typing import Callable

from app.main import app
from app.api import deps


@pytest.fixture(scope="function")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="function")
def get_test_db(db) -> Callable[[], Session]:
    return lambda: db  # type: ignore


@pytest.fixture(scope="function")
def client(get_test_db) -> TestClient:
    """
    Ensure the same database is used on the application side as the tests that construct state.
    """
    try:
        app.dependency_overrides[deps.get_db] = get_test_db
    except AttributeError:
        # By using Sentry middleware, it wraps the app object requiring the
        # actual app be accessed through an additional object also called app.
        app.app.dependency_overrides[deps.get_db] = get_test_db  # type: ignore
    return TestClient(app)
