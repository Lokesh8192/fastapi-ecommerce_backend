from fastapi import status


def test_create_product(client, admin_headers, product_payload,):
    response = client.post(
        "/products",
        json=product_payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["success"] is True
    assert body["data"]["name"] == product_payload["name"].title()
    assert body["data"]["price"] == product_payload["price"]
    assert body["data"]["stock_quantity"] == 50
    assert body["data"]["category_id"] == product_payload["category_id"]


def test_duplicate_product(client, admin_headers, product_payload,):
    first_response = client.post(
        "/products",
        json=product_payload,
        headers=admin_headers,
    )

    assert first_response.status_code == status.HTTP_200_OK

    second_response = client.post(
        "/products",
        json=product_payload,
        headers=admin_headers,
    )

    assert second_response.status_code == status.HTTP_409_CONFLICT


def test_customer_cannot_create_product(client, auth_headers, product_payload,):
    response = client.post(
        "/products",
        json=product_payload,
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_products(
    client,
    auth_headers,
):
    response = client.get(
        "/products",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_get_all_products(
    client,
    auth_headers,
):
    response = client.get(
        "/products/all",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_get_product_by_id(
    client,
    admin_headers,
    product_payload,
):
    create_response = client.post(
        "/products",
        json=product_payload,
        headers=admin_headers,
    )

    assert create_response.status_code == status.HTTP_200_OK

    product_id = create_response.json()["data"]["id"]

    response = client.get(
        f"/products/{product_id}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["success"] is True
    assert body["data"]["id"] == product_id
