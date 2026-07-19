from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import UserResponse

router=APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me",response_model=ApiResponse)
def get_my_profile(
    current_user:User=Depends(get_current_user)
):
    return ApiResponse(
        success=True,
        message="User Profile fetched successfully",
        data=UserResponse.model_validate(current_user),
    )
    
    