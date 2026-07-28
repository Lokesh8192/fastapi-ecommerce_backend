from sqlalchemy import Column, DateTime, func, Enum, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.enums import PaymentStatus, PaymentMethod


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True,)
    payment_reference = Column(
        String(50), unique=True, nullable=False, index=True,)
    order_id = Column(Integer, ForeignKey("orders.id"),
                      nullable=False, unique=True,)
    amount = Column(Numeric(10, 2), nullable=False,)
    payment_method = Column(Enum(PaymentMethod), nullable=False,)
    payment_status = Column(Enum(PaymentStatus),
                            default=PaymentStatus.PENDING, nullable=False,)
    transaction_id = Column(String(100), nullable=True,)
    create_at = Column(DateTime(timezone=True), server_default=func.now(),)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now(),)

    order = relationship(
        "Order",
        back_populates="payment",
    )
