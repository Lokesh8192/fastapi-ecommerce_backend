from datetime import datetime, UTC
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True,)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True,)
    phone_number: Mapped[str | None] = mapped_column(
        String(200), nullable=True,)
    hashed_password: Mapped[str] = mapped_column(nullable=False,)
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, default="customer",)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True,)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC),)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    categories = relationship(
        "Category",
        back_populates="creator",
    )

    products = relationship(
        "Product",
        back_populates="creator",
    )

    cart = relationship(
        "Cart",
        back_populates="user",
        uselist=False,
    )
