from fastapi import APIRouter, Depends, Body, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.depedencies import get_db
from app.core.dependencies import (
    get_current_user,
    get_current_admin,
)

from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.order import OrderStatusUpdateRequest, OrderCreate
from app.services.order_service import order_service
from app.services.email_service import EmailService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "",
    response_model=ApiResponse,
)
def place_order(
    background_tasks: BackgroundTasks,
    request: OrderCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    order = order_service.create_order(
        db=db,
        user_id=current_user.id,
        request=request,
    )

    background_tasks.add_task(
        EmailService.send_order_confirmation,
        current_user.email,
        current_user.username,
        order.order_number,
        order.subtotal,
        order.tax,
        order.shipping_charge,
        order.discount,
        order.grand_total,
    )

    return ApiResponse(
        success=True,
        message="Order placed successfully.",
        data=order,
    )


@router.get("", response_model=ApiResponse)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApiResponse(
        message="Orders fetched successfully.",
        data=order_service.get_orders(
            db,
            current_user.id,
        ),
    )


@router.get("/{order_id}", response_model=ApiResponse)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApiResponse(
        message="Order fetched successfully.",
        data=order_service.get_order_by_id(
            db,
            current_user.id,
            order_id,
        ),
    )


@router.patch(
    "/{order_id}/status",
    response_model=ApiResponse,
)
def update_order_status(
    order_id: int,
    request: OrderStatusUpdateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    order = order_service.update_order_status(
        db=db,
        order_id=order_id,
        status=request.status,
    )

    return ApiResponse(
        success=True,
        message="Order status updated successfully.",
        data=order,
    )
