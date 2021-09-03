import httpx
import pytest

import json

from typing import Optional
from app.core.config import settings


async def make_api_request(
        client: httpx.AsyncClient,
        endpoint: str,
        request: dict,
        auth_token: dict,
        *,
        expected_error: Optional[str] = None,
):
    return (
        await client.post(
            url=f"{settings.SERVER_HOST}/{endpoint}",
            content=json.dumps(request),
            headers={"Content-Type": "application/json", **auth_token},
        ),
        expected_error,
    )


@pytest.mark.asyncio
async def test__example_api__success(get_resource, scaling_auth_token):
    # TODO: Implement
    pass


@pytest.mark.asyncio
async def test__example_api__timeout(get_resource, scaling_auth_token):
    # TODO: Implement
    pass


@pytest.mark.asyncio
async def test__example_api__rate_limited(get_resource, scaling_auth_token):
    # TODO: Implement
    pass
