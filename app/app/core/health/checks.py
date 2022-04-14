from fastapi import Depends

import logging
from aioredis import Redis as RedisConnection  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sentry_sdk import capture_exception

from app.api import deps


def is_database_available(db: Session = Depends(deps.get_db)) -> bool:
    try:
        db.execute("SELECT 1")  # Try to connect to database
    except Exception as e:
        capture_exception(e)
        logging.error(e)
        return False
    return True


async def is_redis_available(
    redis: RedisConnection = Depends(deps.get_redis_connection),
) -> bool:
    try:
        pong = await redis.ping()
    except Exception as e:
        capture_exception(e)
        logging.error(e)
        return False
    return pong


checks = [is_database_available, is_redis_available]
