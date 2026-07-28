from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    order_id: int
    payment_method: PaymentMethod


class PaymentProcessRequest(BaseModel):
    payment_status: PaymentStatus


class PaymentResponse(BaseModel):
    id: int
    payment_reference: str
    order_id: int
    amount: Decimal
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
