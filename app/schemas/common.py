
from pydantic import BaseModel
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T | None = None
    request_id: str | None = None


class StatusUpdate(BaseModel):
    is_active: bool
