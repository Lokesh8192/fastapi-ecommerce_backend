import uuid
import pytest


@pytest.fixture
def user_payload():
    unique = uuid.uuid4().hex[:8]

    return {
        "username": f"user_{unique}",
        "email": f"user_{unique}@test.com",
        "phone_number": "9876543210",
        "password": "Password@123",
        "confirm_password": "Password@123",
    }
