import uuid
import pytest


@pytest.fixture
def product_payload(category_id):
    unique = uuid.uuid4().hex[:8]

    return {
        "name": f"Test Product {unique}",
        "description": "Test product description",
        "price": "999.99",
        "image_url": "https://example.com/product.jpg",
        "category_id": category_id,
        "stock_quantity": 50,
        "is_active": True,
    }
