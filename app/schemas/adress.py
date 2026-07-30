from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AddressCreate(BaseModel):
    full_name: str = Field(..., max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=10)
    address_line1: str = Field(..., max_length=255)
    address_line2: str | None = None
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    postal_code: str = Field(..., min_length=6, max_length=6)
    country: str = "India"
    landmark: str | None = None
    is_default: bool = False


class AddressUpdate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = Field(
        default=None, min_length=10, max_length=10)
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = Field(default=None, min_length=6, max_length=6)
    country: str | None = None
    landmark: str | None = None
    is_default: bool | None = None


class AddressResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone_number: str
    address_line1: str
    address_line2: str | None
    city: str
    state: str
    postal_code: str
    country: str
    landmark: str | None
    is_default: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
