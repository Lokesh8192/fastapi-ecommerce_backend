from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_admin,
    get_current_user,
)
from app.db.depedencies import get_db
from app.models.user import User
from app.schemas.category import (
    CategoryBulkCreate,
    CategoryCreate,
    CategoryUpdate,
)
from app.schemas.common import ApiResponse
from app.schemas.common import StatusUpdate
from app.services.category_service import category_service

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "",
    response_model=ApiResponse,
)
def create_category(
    request: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    category = category_service.create_category(
        db=db,
        request=request,
        current_admin=current_admin,
    )

    return ApiResponse(
        success=True,
        message="Category created successfully.",
        data=category,
    )


@router.post(
    "/bulk",
    response_model=ApiResponse,
)
def create_categories(
    request: CategoryBulkCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    categories = category_service.create_categories(
        db=db,
        request=request,
        current_admin=current_admin,
    )

    return ApiResponse(
        success=True,
        message="Categories created successfully.",
        data=categories,
    )

@router.get(
    "",
    response_model=ApiResponse,
)
def get_all_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    categories = category_service.get_all_categories(
        db=db,
    )

    return ApiResponse(
        success=True,
        message="Categories fetched successfully.",
        data=categories,
    )


@router.get(
    "/{category_id}",
    response_model=ApiResponse,
)
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    category = category_service.get_category_by_id(
        db=db,
        category_id=category_id,
    )

    return ApiResponse(
        success=True,
        message="Category fetched successfully.",
        data=category,
    )


@router.put(
    "/{category_id}",
    response_model=ApiResponse,
)
def update_category(
    category_id: int,
    request: CategoryUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    category = category_service.update_category(
        db=db,
        category_id=category_id,
        request=request,
    )

    return ApiResponse(
        success=True,
        message="Category updated successfully.",
        data=category,
    )

@router.patch(
    "/{category_id}/status",
    response_model=ApiResponse,
)
def update_category_status(
    category_id: int,
    status_data: StatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    category = category_service.update_category_status(
        db=db,
        category_id=category_id,
        is_active=status_data.is_active,
    )

    return ApiResponse(
        success=True,
        message="Category status updated successfully.",
        data=category,
    )