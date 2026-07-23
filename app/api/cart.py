from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.depedencies import get_db
from app.models.user import User
from app.schemas.cart import AddToCartRequest, UpdateCartItemRequest
from app.schemas.common import ApiResponse
from app.services.cart_service import cart_service

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("", response_model=ApiResponse)
def add_to_cart(
    request: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApiResponse(
        message="Product added to cart.",
        data=cart_service.add_to_cart(db, current_user.id, request),
    )


@router.get("", response_model=ApiResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApiResponse(
        message="Cart fetched successfully.",
        data=cart_service.get_cart(db, current_user.id),
    )


@router.put("/{product_id}", response_model=ApiResponse)
def update_cart_item(
    product_id: int,
    request: UpdateCartItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApiResponse(
        message="Cart item updated successfully.",
        data=cart_service.update_item(db, current_user.id, product_id, request),
    )


@router.delete("/{product_id}", response_model=ApiResponse)
def remove_cart_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApiResponse(
        message="Cart item removed successfully.",
        data=cart_service.remove_item(db, current_user.id, product_id),
    )


@router.delete("", response_model=ApiResponse)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_service.clear_cart(db, current_user.id)
    return ApiResponse(message="Cart cleared successfully.")
