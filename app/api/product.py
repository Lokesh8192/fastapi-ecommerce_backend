from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_admin,
    get_current_user,
)
from app.db.depedencies import get_db
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
)
from app.services.product_service import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.post(
    "",
    response_model=ApiResponse,
)
def create_product(
    request: ProductCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    product = product_service.create_product(
        db=db,
        request=request,
        current_admin=current_admin,
    )

    return ApiResponse(
        success=True,
        message="Product created successfully.",
        data=product,
    )
    
@router.get(
    "",
    response_model=ApiResponse,
)
def get_all_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    products = product_service.get_all_products(db)

    return ApiResponse(
        success=True,
        message="Products fetched successfully.",
        data=products,
    )
    
@router.get(
    "/{product_id}",
    response_model=ApiResponse,
)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    product = product_service.get_product_by_id(
        db,
        product_id,
    )

    return ApiResponse(
        success=True,
        message="Product fetched successfully.",
        data=product,
    )
    
@router.put(
    "/{product_id}",
    response_model=ApiResponse,
)
def update_product(
    product_id: int,
    request: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    product = product_service.update_product(
        db=db,
        product_id=product_id,
        request=request,
    )

    return ApiResponse(
        success=True,
        message="Product updated successfully.",
        data=product,
    )
    
@router.patch(
    "/{product_id}/activate",
    response_model=ApiResponse,
)
def activate_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    product = product_service.activate_product(
        db,
        product_id,
    )

    return ApiResponse(
        success=True,
        message="Product activated successfully.",
        data=product,
    )

@router.patch(
    "/{product_id}/deactivate",
    response_model=ApiResponse,
)
def deactivate_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    product = product_service.deactivate_product(
        db,
        product_id,
    )

    return ApiResponse(
        success=True,
        message="Product deactivated successfully.",
        data=product,
    )

