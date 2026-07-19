from datetime import datetime, UTC
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    token: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True,)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False,)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC),)
    user = relationship("User", back_populates="refresh_tokens",)
