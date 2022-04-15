import asyncio
from fastapi import Request
from typing import AsyncGenerator, Generator

import aioredis
from uuid import UUID
from aio_pika import connect_robust

from app.core.config import settings
from app.db.session import SessionLocal


def get_request_id(request: Request) -> UUID:
    return request.state.id


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_amqp_channel() -> AsyncGenerator:
    loop = asyncio.get_event_loop()
    try:
        connection = await connect_robust(settings.AMQP_URI, loop=loop)
        channel = await connection.channel()
        yield channel
    finally:
        await channel.close()


async def get_redis_connection() -> AsyncGenerator:
    try:
        connection = aioredis.from_url(
            settings.REDIS_URI, encoding="utf-8", decode_responses=True
        )
        yield connection.client()
    finally:
        connection.close()
    await connection.wait_closed()


async def get_redis_connection_pool() -> AsyncGenerator:
    try:
        connection_pool = aioredis.from_url(
            settings.REDIS_URI, encoding="utf-8", decode_responses=True
        )
        yield connection_pool
    finally:
        connection_pool.close()
    await connection_pool.wait_closed()
