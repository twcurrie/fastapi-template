import base64
import os

import pytest

from app.core.config import settings
from app.tests.utils import TestType


@pytest.fixture()
def get_resource(get_resource_for_test_type):
    return get_resource_for_test_type(
        test_type=TestType(os.path.dirname(__file__).split("/")[-1])
    )


@pytest.fixture()
def scaling_auth_token() -> dict:
    token = base64.b64encode(
        f"{settings.HTTP_BASIC_AUTH_USERNAME}:{settings.HTTP_BASIC_AUTH_PASSWORD}".encode()
    ).decode("ascii")
    return {"Authorization": f"Basic {token}"}
