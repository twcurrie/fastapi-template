from fastapi.testclient import TestClient


def test__version__not_found(client: TestClient):
    response = client.get(
        "version",
    )
    assert response.status_code == 404
