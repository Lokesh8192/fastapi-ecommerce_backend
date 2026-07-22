from pydantic import BaseModel, Field


class ValidationError(BaseModel):
    field: str = Field(..., examples=["email"])
    message: str = Field(..., examples=["Email is required."])

class ErrorResponse(BaseModel):
    success:bool
    message:str
    errors:list[ValidationError] | None=None