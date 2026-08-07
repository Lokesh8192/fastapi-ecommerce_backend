import uuid
import pytest


@pytest.fixture
def user_payload():
    unique = uuid.uuid4().hex[:8]

    phone_number = str(uuid.uuid4().int % 10_000_000_000).zfill(10)

    return {
        "username": f"user_{unique}",
        "email": f"user_{unique}@test.com",
        "phone_number": phone_number,
        "password": "Password@123",
        "confirm_password": "Password@123",
    }
