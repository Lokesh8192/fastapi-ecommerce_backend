from sqlalchemy import Column, ForeignKey, DateTime, Integer, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True,)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False,)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False,)
    quantity = Column(Integer, nullable=False,)
    price_at_added = Column(Numeric(10, 2), nullable=False,)
    created_at = Column(DateTime(timezone=True), server_default=func.now(),)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now(),)
    cart = relationship(
        "Cart",
        back_populates="items",
    )
    product = relationship(
        "Product",
        back_populates="cart_items",
    )
