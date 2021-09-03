import aioredis  # type: ignore
from sentry_sdk import start_transaction
from typing import AsyncGenerator, Generator

from app.core.config import settings
from app.db.session import SessionLocal


def get_db() -> Generator:
    with start_transaction(op="database"):
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()


async def get_redis_connection() -> AsyncGenerator:
    with start_transaction(op="redis"):
        try:
            connection = await aioredis.create_connection(settings.REDIS_URI)
            yield connection
        finally:
            connection.close()
        await connection.wait_closed()


async def get_redis_connection_pool() -> AsyncGenerator:
    with start_transaction(op="redis_pool"):
        try:
            connection_pool = await aioredis.create_redis_pool(settings.REDIS_URI)
            yield connection_pool
        finally:
            connection_pool.close()
        await connection_pool.wait_closed()
