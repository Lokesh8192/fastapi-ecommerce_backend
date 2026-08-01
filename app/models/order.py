from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.enums import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True,)
    order_number = Column(String(50), unique=True, nullable=False, index=True,)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False,)
    address_id = Column(
        Integer,
        ForeignKey("addresses.id"),
        nullable=False,
    )
    status = Column(Enum(OrderStatus),
                    default=OrderStatus.PENDING, nullable=False,)
    subtotal = Column(Numeric(10, 2), default=0, nullable=False,)
    tax = Column(Numeric(10, 2), default=0, nullable=False,)
    shipping_charge = Column(Numeric(10, 2), default=0, nullable=False,)
    discount = Column(Numeric(10, 2), default=0, nullable=False,)
    grand_total = Column(Numeric(10, 2), default=0, nullable=False,)
    created_at = Column(DateTime(timezone=True), server_default=func.now(),)
    updated_at = Column(DateTime(timezone=True,),
                        server_default=func.now(), onupdate=func.now(),)

    user = relationship(
        "User",
        back_populates="orders",
    )

    address = relationship(
        "Address",
        back_populates="orders",
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
    )
