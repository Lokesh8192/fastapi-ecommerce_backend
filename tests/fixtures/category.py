import uuid
import pytest


@pytest.fixture
def category_payload():
    unique = uuid.uuid4().hex[:8]

    return {
        "name": f"Category_{unique}",
        "description": "Test Category",
    }
