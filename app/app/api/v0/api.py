from fastapi import APIRouter, Depends

from app.api.v0.endpoints import example
from app.api.v0.endpoints import patient
from app.core.security import authenticate_http_basic

api_router = APIRouter(dependencies=[Depends(authenticate_http_basic)],)
api_router.include_router(example.router, prefix="/example", tags=["example"])
api_router.include_router(patient.router, prefix="/patients", tags=["patient"])
