import os

import pytest
from app.tests.utils import TestType


@pytest.fixture()
def get_resource(get_resource_for_test_type):
    return get_resource_for_test_type(
        test_type=TestType(os.path.dirname(__file__).split("/")[-1])
    )
