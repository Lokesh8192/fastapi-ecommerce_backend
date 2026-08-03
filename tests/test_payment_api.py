from decimal import Decimal
from types import SimpleNamespace

from fastapi import BackgroundTasks

from app.api.payment import EmailService, process_payment
from app.models.enums import PaymentStatus


def test_process_payment_endpoint_returns_processed_payment(monkeypatch):
    background_tasks = BackgroundTasks()

    dummy_payment = SimpleNamespace(
        payment_status=PaymentStatus.SUCCESS,
        payment_reference="REF123",
        order_id=1,
        amount=Decimal("150.00"),
        payment_method=SimpleNamespace(value="CARD"),
    )

    dummy_order = SimpleNamespace(
        user=SimpleNamespace(email="test@example.com", username="adminuser"),
        order_number="ORDER-001",
    )

    monkeypatch.setattr(
        "app.api.payment.payment_service.process_payment",
        lambda db, payment_id, payment_status: dummy_payment,
    )
    monkeypatch.setattr(
        "app.api.payment.payment_service.order_repository.get_order_by_id",
        lambda db, order_id: dummy_order,
    )

    result = process_payment(
        payment_id=1,
        background_tasks=background_tasks,
        payment_status=PaymentStatus.SUCCESS,
        db=None,
        current_user=SimpleNamespace(role="ADMIN"),
    )

    assert result is dummy_payment
    assert background_tasks.tasks, "Background task should be scheduled for successful payment"
    assert background_tasks.tasks[0][0] == EmailService.send_payment_success
