import uuid
import pytest


@pytest.fixture
def category_payload():
    unique = uuid.uuid4().hex[:8]

    return {
        "name": f"Category_{unique}",
        "description": "Test Category",
    }

@pytest.fixture
def category_id(
    client,
    admin_headers,
    category_payload,
):
    response = client.post(
        "/categories",
        json=category_payload,
        headers=admin_headers,
    )

    assert response.status_code == 201

    return response.json()["data"]["id"]