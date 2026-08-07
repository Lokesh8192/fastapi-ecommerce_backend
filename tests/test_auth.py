from fastapi import status


def test_register_user(
    client,
    user_payload,
):
    response = client.post(
        "/auth/register",
        json=user_payload,
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "User registered successfully."

    assert data["data"]["username"] == user_payload["username"]
    assert data["data"]["email"] == user_payload["email"]


def test_register_duplicate_email(client, user_payload,):
    client.post("/auth/register", json=user_payload,)

    duplicate = user_payload.copy()
    duplicate["username"] = "another_user"

    response = client.post(
        "/auth/register",
        json=duplicate,
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_register_duplicate_username(client, user_payload,):

    client.post("/auth/register", json=user_payload,)

    duplicate = user_payload.copy()
    duplicate["email"] = "another@test.com"

    response = client.post(
        "/auth/register",
        json=duplicate,
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_login_success(login_response,):
    assert login_response["success"] is True

    assert "access_token" in login_response["data"]
    assert "refresh_token" in login_response["data"]


def test_login_wrong_password(client, registered_user):
    response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": "WrongPassword"
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token(client, refresh_token):
    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    assert "access_token" in response.json()["data"]


def test_logout(client, refresh_token):
    response = client.post(
        "/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == status.HTTP_200_OK
