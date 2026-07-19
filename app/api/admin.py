from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard", response_model=ApiResponse)
def admin_dashboard(
    current_admin: User = Depends(get_current_admin),
):
    return ApiResponse(
        success=True,
        message="Welcome Admin",
        data=UserResponse.model_validate(current_admin),
    )
