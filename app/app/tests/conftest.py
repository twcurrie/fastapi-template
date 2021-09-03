import os
from base64 import b64encode
from pathlib import Path

from faker import Faker

import pytest

from app.core.config import settings
from app.tests.utils import TestType


def encoded_token():
    return b64encode(
        bytes(
            f"{settings.HTTP_BASIC_AUTH_USERNAME}:{settings.HTTP_BASIC_AUTH_PASSWORD}",
            encoding="ascii",
        )
    ).decode("ascii")


@pytest.fixture(scope="function")
def basic_auth_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_token()}",
    }


@pytest.fixture
def random_name(get_random_name):
    return get_random_name()


@pytest.fixture
def get_random_name():
    def create_random_name():
        fake = Faker("en_us")
        return fake.name()

    return create_random_name


@pytest.fixture
def random_date(get_random_date):
    return get_random_date()


@pytest.fixture
def get_random_date():
    def create_random_date():
        fake = Faker("en_us")
        return fake.date()

    return create_random_date


@pytest.fixture
def get_resource_for_test_type():
    """
    Generalized resource getter for test subdirectories.
    """

    def test_type_resource_getter(test_type: TestType):
        def resource_getter(resource: Path):
            root_dir = f"{os.path.dirname(os.path.abspath(__file__))}"
            resources_dir = f"{root_dir}/{test_type.value}/resources"
            if (Path(resources_dir) / resource).is_file():
                return open(Path(resources_dir) / resource)
            elif (Path(f"{root_dir}/resources") / resource).is_file():
                return open(Path(f"{root_dir}/resources") / resource)
            else:
                raise ValueError(f"Unknown resource specified: {resource}")

        return resource_getter

    return test_type_resource_getter


def pytest_collection_modifyitems(config, items):
    """
    Dynamically add test subdirectory (ie, `unit`, `end_to_end`) as marker
    """
    rootdir = Path(config.rootdir)

    def get_test_suite_name(path: Path):
        if path.parent.name == "tests":
            return path.name
        return get_test_suite_name(path.parent)

    for item in items:
        mark_name = get_test_suite_name(Path(item.fspath).relative_to(rootdir))
        mark = getattr(pytest.mark, mark_name)
        item.add_marker(mark)
