from typing import List, Optional

from fastapi import APIRouter, Request
from sqlalchemy.orm import Session  # type: ignore

from app.core.controls import rate_limiter
from app.domain import example_api
from app.core.logging import get_logger

router = APIRouter()
shared_limit = rate_limiter.shared_limit("5/minute", "from-downstream")


@router.get("/")
@rate_limiter.exempt
def get_string(request: Request,) -> str:  # noqa: Attribute used by rate limiter
    return "dummy"


@router.get("/from-downstream")
@shared_limit
async def get_strings_from_downstream(request: Request) -> List[str]:
    return await get_multiple_strings_from_downstream(request)


@router.get("/from-downstream/{id}")
@shared_limit
async def get_multiple_strings_from_downstream(
    request: Request, id: Optional[int] = None  # noqa: Attribute used by rate limiter
) -> List[str]:
    logger = get_logger(__name__)
    logger.info(
        f"Received GET request for {id} checks.", extra={"request.id": request.state.id}
    )
    response = await example_api.get_status_checks(number_of_checks=id)
    return response


@router.get("/{id}")
@rate_limiter.limit("1/minute")
def get_string_by_id(
    request: Request, id: int  # noqa: Attribute used by rate limiter
) -> str:
    logger = get_logger(__name__)
    logger.info(
        f"Received GET request for {id}.", extra={"request.id": request.state.id}
    )
    return f"dummy {id}"
