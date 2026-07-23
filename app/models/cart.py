from sqlalchemy import Column, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Cart(Base):

    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True,)
    user_id = Column(Integer, ForeignKey("users.id"),
                     nullable=False, unique=True,)
    created_at = Column(DateTime(timezone=True), server_default=func.now(),)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now(),)
    user = relationship(
        "User",
        back_populates="cart",
    )
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )
