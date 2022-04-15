import os
from typing import Generator

import aioredis
import pytest
from aioredis import Redis as RedisConnection  # type: ignore
from sqlalchemy import orm  # type: ignore
from sqlalchemy.engine import Connection  # type: ignore

from app.core.config import settings
from app.db.session import engine
from app.tests.utils import TestType

Session = orm.sessionmaker()


@pytest.fixture(scope="module")
def connection() -> Connection:
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def db(connection) -> orm.Session:
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session  # type: ignore
    session.close()
    transaction.rollback()


@pytest.fixture(scope="function")
def redis() -> Generator:
    connection = aioredis.from_url(
        settings.REDIS_URI, encoding="utf-8", decode_responses=True
    )
    yield connection


@pytest.fixture()
def get_resource(get_resource_for_test_type):
    return get_resource_for_test_type(
        test_type=TestType(os.path.dirname(__file__).split("/")[-1])
    )
