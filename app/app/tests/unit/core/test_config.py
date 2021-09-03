import pytest
from pydantic import ValidationError
from app.core.config import Settings


def test__in_testing_environment():
    settings = Settings()
    assert settings.ENVIRONMENT.is_testing()


def test__redis_uri__string_provided__success():
    redis_uri = "redis://:not_a_password@localhost:6379/0"

    settings = Settings(REDIS_URI=redis_uri)
    assert f"{settings.REDIS_URI}" == redis_uri


def test__app_database_uri__string_provided__success():
    postgres_uri = "postgresql://user:password@localhost:5432/database"

    settings = Settings(APP_DATABASE_URI=postgres_uri)
    assert f"{settings.APP_DATABASE_URI}" == postgres_uri
