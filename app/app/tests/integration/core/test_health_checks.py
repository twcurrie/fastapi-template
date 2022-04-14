import pytest
from app.core.health.checks import is_database_available, is_redis_available


def test__database__health(db):
    assert is_database_available(db)


@pytest.mark.asyncio
async def test__redis__health(redis):
    assert await is_redis_available(redis)
