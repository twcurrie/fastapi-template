from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from app.core.config import settings

security = HTTPBasic()


def authenticate_http_basic(
    credentials: HTTPBasicCredentials = Depends(security),
) -> bool:
    correct_username = secrets.compare_digest(
        credentials.username, settings.HTTP_BASIC_AUTH_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.HTTP_BASIC_AUTH_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True
