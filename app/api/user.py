from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.depedencies import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import UserResponse,UserUpdate,ChangePasswordRequest
from app.services.user_service import user_service

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
    
@router.put(
    "/me",
    response_model=ApiResponse,
)
def update_profile(
    request: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_user = user_service.update_profile(
        db=db,
        current_user=current_user,
        request=request,
    )

    return ApiResponse(
        success=True,
        message="Profile updated successfully.",
        data=updated_user,
    )
    
@router.put(
    "/change-password",
    response_model=ApiResponse,
)
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service.change_password(
        db=db,
        current_user=current_user,
        request=request,
    )

    return ApiResponse(
        success=True,
        message="Password changed successfully.",
    )

@router.delete(
    "/me",
    response_model=ApiResponse,
)
def deactivate_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service.deactivate_account(
        db=db,
        current_user=current_user,
    )

    return ApiResponse(
        success=True,
        message="Account deactivated successfully.",
    )