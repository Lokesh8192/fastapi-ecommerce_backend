from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from decimal import Decimal
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
    StockUpdate,
)
from app.schemas.common import StatusUpdate
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
def get_products(
    search: str | None = None,
    category_id: int | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    products = product_service.get_products(
        db=db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        order=order,
        page=page,
        size=size,
    )

    return ApiResponse(
        success=True,
        message="Products fetched successfully.",
        data=products,
    )


@router.get(
    "/all",
    response_model=ApiResponse,
)
def get_all_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    products = product_service.get_all_products(db)

    return ApiResponse(
        success=True,
        message="All products fetched successfully.",
        data=products,
    )


@router.get(
    "/low-stock",
    response_model=ApiResponse,
)
def get_low_stock_products(
    threshold: int = 10,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    products = product_service.get_low_stock_products(
        db=db,
        threshold=threshold,
    )

    return ApiResponse(
        success=True,
        message="Low stock products fetched successfully.",
        data=products,
    )


@router.get(
    "/out-of-stock",
    response_model=ApiResponse,
)
def get_out_of_stock_products(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    products = product_service.get_out_of_stock_products(db)

    return ApiResponse(
        success=True,
        message="Out of stock products fetched successfully.",
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
        db=db,
        product_id=product_id,
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
    "/{product_id}/status",
    response_model=ApiResponse,
)
def update_product_status(
    product_id: int,
    status_data: StatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    product = product_service.update_product_status(
        db=db,
        product_id=product_id,
        is_active=status_data.is_active,
    )

    return ApiResponse(
        success=True,
        message="Product status updated successfully.",
        data=product,
    )


@router.patch(
    "/{product_id}/stock",
    response_model=ApiResponse,
)
def update_product_stock(
    product_id: int,
    request: StockUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    product = product_service.update_stock(
        db=db,
        product_id=product_id,
        stock_quantity=request.stock,
    )

    return ApiResponse(
        success=True,
        message="Product stock updated successfully.",
        data=product,
    )
