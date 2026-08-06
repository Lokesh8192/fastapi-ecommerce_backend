import asyncio

from app.core.celery_app import celery_app
from app.services.email_service import EmailService


@celery_app.task
def send_welcome_email_task(
    email: str,
    full_name: str,
):
    asyncio.run(
        EmailService.send_welcome_email(
            email=email,
            full_name=full_name,
        )
    )


@celery_app.task
def send_order_confirmation_email_task(
    email: str,
    username: str,
    order_number: str,
    subtotal,
    tax,
    shipping_charge,
    discount,
    grand_total,
):
    asyncio.run(
        EmailService.send_order_confirmation(
            email=email,
            username=username,
            order_number=order_number,
            subtotal=subtotal,
            tax=tax,
            shipping_charge=shipping_charge,
            discount=discount,
            grand_total=grand_total,
        )
    )


@celery_app.task
def send_payment_success_email_task(
    email: str,
    username: str,
    payment_reference: str,
    order_number: str,
    amount,
    payment_method: str,
):
    asyncio.run(
        EmailService.send_payment_success(
            email=email,
            username=username,
            payment_reference=payment_reference,
            order_number=order_number,
            amount=amount,
            payment_method=payment_method,
        )
    )
