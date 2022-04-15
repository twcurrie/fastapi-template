import asyncio
import httpx

from typing import List, Optional
from pydantic import ValidationError
from ddtrace import tracer

from app.core.config import settings
from app.core.exceptions import ApiTimeoutError, ApiSerializationError
from app.schemas.external.example_api import StatusCheck


@tracer.wrap()
async def request_status_check(client: httpx.AsyncClient) -> StatusCheck:
    try:
        response = await client.get(f"{settings.EXAMPLE_API_ENDPOINT}/status-check")
    except httpx.ReadTimeout as e:
        raise ApiTimeoutError(e, api_endpoint=str(settings.EXAMPLE_API_ENDPOINT))
    try:
        return StatusCheck(**response.json())
    except ValidationError as e:
        raise ApiSerializationError(e, api_endpoint=str(settings.EXAMPLE_API_ENDPOINT))


@tracer.wrap()
async def get_status_checks(number_of_checks: Optional[int] = None) -> List[str]:
    async with httpx.AsyncClient() as client:
        return [
            response.value
            for response in await asyncio.gather(
                *[request_status_check(client) for _ in range(number_of_checks or 1)],
                return_exceptions=False,
            )
        ]
