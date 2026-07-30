from sqlalchemy import Integer, ForeignKey, Boolean, String, Column, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True,)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False,)
    full_name = Column(String(100), nullable=False,)
    phone_number = Column(String(15), nullable=False,)
    address_line1 = Column(String(255), nullable=False,)
    address_line2 = Column(String(255), nullable=False,)
    city = Column(String(100), nullable=False,)
    state = Column(String(100), nullable=False,)
    postal_code = Column(String(10), nullable=False,)
    country = Column(String(100), nullable=False, default="India",)
    landmark = Column(String(255), nullable=False,)
    is_default = Column(Boolean, nullable=False, default=False,)
    created_at = Column(DateTime(timezone=True), server_default=func.now(),)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now(),)

    user = relationship("User", back_populates="addresses",)
