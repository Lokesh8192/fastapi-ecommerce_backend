from fastapi import APIRouter, Depends, Query, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.depedencies import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.enums import PaymentStatus
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import payment_service
from app.services.email_service import EmailService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    request: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return payment_service.create_payment(
        db=db,
        user_id=current_user.id,
        request=request,
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment_by_id(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return payment_service.get_payment_by_id(
        db=db,
        user_id=current_user.id,
        payment_id=payment_id,
    )


@router.get(
    "/order/{order_id}",
    response_model=PaymentResponse,
)
def get_payment_by_order_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return payment_service.get_payment_by_order_id(
        db=db,
        user_id=current_user.id,
        order_id=order_id,
    )


@router.patch(
    "/{payment_id}/process",
    response_model=PaymentResponse,
)
def process_payment(
    payment_id: int,
    background_tasks: BackgroundTasks,
    payment_status: PaymentStatus = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):

    payment = payment_service.process_payment(
        db=db,
        payment_id=payment_id,
        payment_status=payment_status,
    )

    order = payment_service.order_repository.get_order_by_id(
        db,
        payment.order_id,
    )

    if payment.payment_status == PaymentStatus.SUCCESS:
        background_tasks.add_task(
            EmailService.send_payment_success,
            order.user.email,
            order.user.username,
            payment.payment_reference,
            order.order_number,
            payment.amount,
            payment.payment_method.value,
        )

    return payment
