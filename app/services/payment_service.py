from uuid import uuid4

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import BadRequestException, NotFoundException
from app.models.enums import OrderStatus, PaymentStatus
from app.models.payment import Payment
from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.utils.payment_reference import generate_payment_reference
from app.services.product_service import ProductService


class PaymentService:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        order_repository: OrderRepository,
    ):
        self.payment_repository = payment_repository
        self.order_repository = order_repository

    @staticmethod
    def _to_response(payment: Payment) -> PaymentResponse:
        return PaymentResponse(
            id=payment.id,
            payment_reference=payment.payment_reference,
            order_id=payment.order_id,
            amount=payment.amount,
            payment_method=payment.payment_method,
            payment_status=payment.payment_status,
            transaction_id=payment.transaction_id,
            created_at=payment.create_at,
            updated_at=payment.updated_at,
        )

    def create_payment(
        self,
        db: Session,
        user_id: int,
        request: PaymentCreate,
    ) -> PaymentResponse:
        """Create a pending payment for an order owned by the current user."""
        order = self.order_repository.get_order_by_id(db, request.order_id)
        if not order or order.user_id != user_id:
            raise NotFoundException("Order not found.")
        if order.status != OrderStatus.PENDING:
            raise BadRequestException(
                "Payments can only be created for pending orders.")
        if self.payment_repository.get_payment_by_order_id(db, order.id):
            raise BadRequestException(
                "A payment already exists for this order.")

        try:
            payment = self.payment_repository.create_payment(
                db,
                Payment(
                    payment_reference=generate_payment_reference(),
                    order_id=order.id,
                    amount=order.grand_total,
                    payment_method=request.payment_method,
                    payment_status=PaymentStatus.PENDING,
                ),
            )
            db.commit()
            db.refresh(payment)
        except Exception:
            db.rollback()
            raise

        return self._to_response(payment)

    def get_payment_by_id(
        self,
        db: Session,
        user_id: int,
        payment_id: int,
    ) -> PaymentResponse:
        payment = self.payment_repository.get_payment_by_id(db, payment_id)
        if not payment:
            raise NotFoundException("Payment not found.")

        order = self.order_repository.get_order_by_id(db, payment.order_id)
        if not order or order.user_id != user_id:
            raise NotFoundException("Payment not found.")
        return self._to_response(payment)

    def get_payment_by_order_id(
        self,
        db: Session,
        user_id: int,
        order_id: int,
    ) -> PaymentResponse:
        order = self.order_repository.get_order_by_id(db, order_id)
        if not order or order.user_id != user_id:
            raise NotFoundException("Order not found.")

        payment = self.payment_repository.get_payment_by_order_id(db, order_id)
        if not payment:
            raise NotFoundException("Payment not found.")
        return self._to_response(payment)

    def process_payment(
        self,
        db: Session,
        payment_id: int,
        payment_status: PaymentStatus,
    ) -> PaymentResponse:

        print("=" * 60)
        print("Payment ID received:", payment_id)

        """Record a processor result and update the order when payment succeeds."""
        payment = self.payment_repository.get_payment_by_id(db, payment_id)

        print("Payment object:", payment)

        if payment:
            print("Payment DB ID:", payment.id)
            print("Order ID:", payment.order_id)

        print("=" * 60)

        if not payment:
            raise NotFoundException("Payment not found.")

        allowed_transitions = {
            PaymentStatus.PENDING: {PaymentStatus.SUCCESS, PaymentStatus.FAILED},
            PaymentStatus.SUCCESS: {PaymentStatus.REFUNDED},
        }
        if payment_status not in allowed_transitions.get(payment.payment_status, set()):
            raise BadRequestException(
                f"Cannot change payment status from {payment.payment_status.value} "
                f"to {payment_status.value}."
            )

        order = self.order_repository.get_order_by_id(db, payment.order_id)
        if not order:
            raise NotFoundException("Order not found.")

        try:
            payment.payment_status = payment_status

            if payment_status == PaymentStatus.SUCCESS:
                payment.transaction_id = f"TXN-{uuid4().hex.upper()}"

                # Validate stock
                for item in order.items:
                    ProductService.validate_stock(
                        product=item.product,
                        quantity=item.quantity,
                    )

                # Deduct stock
                for item in order.items:
                    ProductService.deduct_stock(
                        db=db,
                        product=item.product,
                        quantity=item.quantity,
                    )

                order.status = OrderStatus.CONFIRMED

            elif payment_status == PaymentStatus.REFUNDED:

                if order.status != OrderStatus.DELIVERED:
                    raise BadRequestException(
                        "Only delivered orders can be refunded."
                    )

                # Restore stock
                for item in order.items:
                    ProductService.restore_stock(
                        db=db,
                        product=item.product,
                        quantity=item.quantity,
                    )

                order.status = OrderStatus.RETURNED

            self.payment_repository.update_payment(db, payment)
            self.order_repository.update_order(db, order)

            db.commit()
            db.refresh(payment)

        except Exception:
            db.rollback()
            raise

        return self._to_response(payment)


payment_service = PaymentService(PaymentRepository(), OrderRepository())
