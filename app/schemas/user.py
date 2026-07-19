from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


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
        max_length=20,
    )


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="password must be btw 8 & 128 chars!",
    )

    confirm_password: str

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
