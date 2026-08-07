import pytest
import uuid
from app.db.database import SessionLocal
from app.repositories.user_repository import UserRepository
from app.core.roles import UserRole


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


@pytest.fixture
def admin_headers(client):
    unique = uuid.uuid4().hex[:8]

    admin_payload = {
        "username": f"admin_{unique}",
        "email": f"admin_{unique}@test.com",
        "phone_number": str(uuid.uuid4().int % 10_000_000_000).zfill(10),
        "password": "Password@123",
        "confirm_password": "Password@123",
        "role": UserRole.ADMIN.value,
    }

    register = client.post(
        "/auth/register",
        json=admin_payload,
    )

    assert register.status_code == 201

    login = client.post(
        "/auth/login",
        json={
            "email": admin_payload["email"],
            "password": admin_payload["password"],
        },
    )

    assert login.status_code == 200

    token = login.json()["data"]["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }