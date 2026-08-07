from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator
from app.core.roles import UserRole
from typing import Optional
import re


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username must be between 3 and 50 chars.",
    )

    # email must be with @gmail, @outlook, @yahoo
    email: EmailStr = Field(
        ...,
        description="Email must be a valid email address.",
    )

    phone_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=20,
        description="Phone Number must be at least 10 digits.",
    )


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="password must be btw 8 & 128 chars!",
    )

    confirm_password: str

    role: Optional[UserRole] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise ValueError(
                "Password must contain at least one uppercase letter!")
        if not any(char.islower() for char in value):
            raise ValueError(
                "Password must contain at least one lowercase letter!")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit!")
        if not any(char in "@$!%*?&" for char in value):
            raise ValueError(
                "Password must contain at least one special character."
            )
        return value

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, value: str, info):
        password = info.data.get("password")

        if password != value:
            raise ValueError("Password does not match!")

        return value


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Username",
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if value is None:
            return value

        pattern = r"^[A-Za-z][A-Za-z0-9_]*$"

        if not re.match(pattern, value):
            raise ValueError(
                "Username must start with a letter and contain only letters, numbers, and underscores."
            )

    phone_number: str | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        if value is None:
            return value

        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")

        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")

        return value

    @model_validator(mode="after")
    def validate_update_request(self):
        if self.username is None and self.phone_number is None:
            raise ValueError(
                "At least one field must be provided."
            )

        return self


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(...)

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New Password",
    )
    confirm_password: str = Field(...)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain at least one number."
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "Password must contain at least one special character."
            )

        return value

    @model_validator(mode="after")
    def validate_confirm_password(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Password do not match")
        return self


class UserRoleUpdate(BaseModel):
    role: UserRole
