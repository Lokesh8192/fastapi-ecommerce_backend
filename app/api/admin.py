from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_admin
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import UserRoleUpdate
from app.schemas.user import UserResponse
from app.services.user_service import user_service

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


@router.get("/users", response_model=ApiResponse,)
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    users = user_service.get_all_users(db)

    return ApiResponse(
        success=True,
        message="User Fetched Successfully.",
        data=users,
    )


@router.get("/users/{user_id}", response_model=ApiResponse,)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin),):
    user = user_service.get_user_by_id(
        db,
        user_id,
    )

    return ApiResponse(
        success=True,
        message="User Fetched Successfully",
        data=user,
    )


@router.put("/users/{user_id}/role", response_model=ApiResponse,)
def update_user_role(
    user_id: int,
    request: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = user_service.update_role(
        db=db,
        current_admin=current_admin,
        user_id=user_id,
        request=request,
    )

    return ApiResponse(
        success=True,
        message="User Role updated successfully",
        data=user,
    )


@router.patch("/users/{user_id}/activate", response_model=ApiResponse)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = user_service.activate_user(
        db=db,
        user_id=user_id,
    )

    return ApiResponse(
        success=True,
        message="User Activated Successfully",
        data=user,
    )


@router.patch("/users/{user_id}/deactivate", response_model=ApiResponse,)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = user_service.deactivate_user(
        db=db,
        current_admin=current_admin,
        user_id=user_id,
    )

    return ApiResponse(
        success=True,
        message="User Deactivated Successfully",
        data=user,
    )
