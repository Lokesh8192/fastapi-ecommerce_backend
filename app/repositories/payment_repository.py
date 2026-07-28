from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    def create_payment(
        self,
        db: Session,
        payment: Payment,
    ) -> Payment:
        db.add(payment)
        db.flush()
        db.refresh(payment)
        return payment

    def get_payment_by_id(
        self,
        db: Session,
        payment_id: int,
    ) -> Payment | None:
        return (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

    def get_payment_by_order_id(
        self,
        db: Session,
        order_id: int,
    ) -> Payment | None:
        return (
            db.query(Payment)
            .filter(Payment.order_id == order_id)
            .first()
        )

    def get_payment_by_reference(
        self,
        db: Session,
        payment_reference: str,
    ) -> Payment | None:
        return (
            db.query(Payment)
            .filter(
                Payment.payment_reference == payment_reference
            )
            .first()
        )

    def update_payment(
        self,
        db: Session,
        payment: Payment,
    ) -> Payment:
        db.flush()
        db.refresh(payment)
        return payment

    def delete_payment(
        self,
        db: Session,
        payment: Payment,
    ) -> None:
        db.delete(payment)
        db.flush()
