from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True,)
    name = Column(
        String(150),
        nullable=False,
        index=True,
    )
    description = Column(Text, nullable=False,)
    price = Column(Numeric(10, 2), nullable=False,)
    stock = Column(Integer, nullable=False, default=0,)
    image_url = Column(String(500), nullable=True,)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False,)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False,)
    is_active = Column(Boolean, default=True, nullable=False,)
    created_at = Column(DateTime(timezone=True), server_default=func.now(),)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now(),)
    category = relationship("Category", back_populates="products",)
    creator = relationship("User", back_populates="products",)
