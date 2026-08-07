from fastapi import status


def test_create_category(client, admin_headers, category_payload,):
    response = client.post(
        "/categories",
        json=category_payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["success"] is True
    assert data["data"]["name"] == category_payload["name"]


def test_duplicate_category(
    client,
    admin_headers,
    category_payload,
):
    client.post(
        "/categories",
        json=category_payload,
        headers=admin_headers,
    )

    response = client.post(
        "/categories",
        json=category_payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_categories(
    client,
):
    response = client.get("/categories")

    assert response.status_code == status.HTTP_200_OK


def test_customer_cannot_create_category(
    client,
    auth_headers,
    category_payload,
):
    response = client.post(
        "/categories",
        json=category_payload,
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
