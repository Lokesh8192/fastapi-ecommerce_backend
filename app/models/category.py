from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True,)
    description = Column(Text, nullable=False,)
    is_active = Column(Boolean, default=True, nullable=False,)
    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now(),)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now(),)

    creator = relationship(
        "User",
        back_populates="categories",
    )

    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
    )
