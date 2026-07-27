from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel

from app.models.enums import OrderStatus

class OrderItemResponse(BaseModel):
    product_id:int
    product_name:str
    quantity:int
    unit_price:Decimal
    total_price:Decimal
    
class OrderResponse(BaseModel):
    order_id: int
    order_number: str
    status: OrderStatus
    subtotal: Decimal
    tax: Decimal
    shipping_charge: Decimal
    discount: Decimal
    grand_total: Decimal
    created_at: datetime
    items: list[OrderItemResponse]

class OrderSummaryResponse(BaseModel):
    order_id:int
    order_number:str
    status:OrderStatus
    grand_total:Decimal
    created_at:datetime

class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus