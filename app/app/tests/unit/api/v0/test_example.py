import pytest

from fastapi.testclient import TestClient

from app.core.exceptions import ApiSerializationError, ApiTimeoutError


def test__get_example_string__success(client: TestClient, basic_auth_headers: dict):
    response = client.get("api/v0/example", headers=basic_auth_headers)
    assert response.status_code == 200
    assert response.json() == "dummy"


@pytest.mark.asyncio
def test__get_example_string_from_downstream__success(
        client: TestClient, mock_example_api, basic_auth_headers: dict
):
    response = client.get(
        "api/v0/example/from-downstream",
        headers=basic_auth_headers,
    )
    assert response.status_code == 200
    assert response.json() == ["All good!"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "side_effect, expected_message, expected_status_code",
    [
        (ApiTimeoutError("Some issue..."), "Supporting API is not available.", 504),
        (
                ApiSerializationError("Some issue..."),
                "Response from supporting API can not be parsed.",
                424,
        ),
    ],
)
def test__get_example_string_from_downstream__fails(
    client: TestClient,
    failing_mock_example_api,
    expected_message: str,
    expected_status_code: int,
    basic_auth_headers: dict,
):
    response = client.get(
        "api/v0/example/from-downstream",
        headers=basic_auth_headers,
    )
    assert response.status_code == expected_status_code
    assert response.json()["message"] == expected_message


@pytest.mark.parametrize(
    "id, expected_string", [(1, "dummy 1"), (10, "dummy 10"), (99, "dummy 99")]
)
def test__get_example_string_by_id__success(
    client: TestClient, id: int, expected_string: str, basic_auth_headers: dict
):
    response = client.get(
        f"api/v0/example/{id}",
        headers=basic_auth_headers,
    )
    assert response.status_code == 200
    assert response.json() == expected_string
