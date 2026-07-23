from pydantic import BaseModel, Field
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class AddToCartRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):

    product_id: int

    product_name: str

    quantity: int

    unit_price: Decimal

    total_price: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class CartResponse(BaseModel):

    cart_id: int

    total_items: int

    subtotal: Decimal

    items: list[CartItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )
