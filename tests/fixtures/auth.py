import pytest


@pytest.fixture
def registered_user(
    client,
    user_payload,
):
    response = client.post(
        "/auth/register",
        json=user_payload,
    )
    assert response.status_code == 201
    return user_payload


@pytest.fixture
def login_response(
    client,
    registered_user,
):
    response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def access_token(
    login_response
):
    return login_response["data"]["access_token"]


@pytest.fixture
def refresh_token(login_response):
    return login_response["data"]["refresh_token"]


@pytest.fixture
def auth_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}"
    }
