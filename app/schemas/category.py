from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Category name",
    )

    description: str | None = Field(
        default=None,
        max_length=500,
        description="Category Description",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError(
                "Category name cannot be empty."
            )

        return value


class CategoryCreate(CategoryBase):
    pass


class CategoryBulkCreate(BaseModel):
    categories: list[CategoryCreate] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Categories to create in one request.",
    )

    @model_validator(mode="after")
    def validate_unique_names(self):
        names = [category.name.casefold() for category in self.categories]
        if len(names) != len(set(names)):
            raise ValueError("Each category name must be unique within the request.")
        return self


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )

    @model_validator(mode="after")
    def validate_update(self):
        if self.name is None and self.description is None:
            raise ValueError(
                "At least one field must be provided."
            )
        return self


class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

