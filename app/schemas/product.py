from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    price: Decimal = Field(
        ...,
        gt=0,
    )

    stock: int = Field(
        ...,
        ge=0,
    )
    image_url: str | None = Field(
        default=None,
        max_length=500,
        description="Product image URL.",
    )
    category_id: int

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if not value:
            return None

        if not value.startswith(("http://", "https://")):
            raise ValueError("image_url must be a valid http or https URL.")

        return value


class ProductCreate(ProductBase):

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "Product name cannot be empty."
            )

        return value.title()


class ProductUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=150,
    )

    description: str | None = None

    price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    stock: int | None = Field(
        default=None,
        ge=0,
    )

    image_url: str | None = Field(
        default=None,
        max_length=500,
        description="Product image URL.",
    )

    category_id: int | None = None

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if not value:
            return None

        if not value.startswith(("http://", "https://")):
            raise ValueError("image_url must be a valid http or https URL.")

        return value

    @model_validator(mode="after")
    def validate_update(self):

        if all(
            value is None
            for value in [
                self.name,
                self.description,
                self.price,
                self.stock,
                self.image_url,
                self.category_id,
            ]
        ):
            raise ValueError(
                "At least one field must be provided."
            )

        return self


class ProductResponse(ProductBase):

    id: int

    created_by: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
