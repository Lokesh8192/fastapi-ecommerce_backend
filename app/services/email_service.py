from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent

template_env = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    USE_CREDENTIALS=True,
)


class EmailService:

    @staticmethod
    async def send_email(
        recipients: list[str],
        subject: str,
        template_name: str,
        context: dict,
    ) -> None:

        template = template_env.get_template(template_name)
        html = template.render(**context)

        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=html,
            subtype=MessageType.html,
        )

        fm = FastMail(conf)

        await fm.send_message(message)

    @staticmethod
    async def send_welcome_email(
        email: str,
        full_name: str,
    ):
        await EmailService.send_email(
            recipients=[email],
            subject="Welcome to E-Commerce Backend",
            template_name="welcome.html",
            context={
                "full_name": full_name,
            },
        )

    @staticmethod
    async def send_order_confirmation(
        email: str,
        username: str,
        order_number: str,
        subtotal,
        tax,
        shipping_charge,
        discount,
        grand_total,
    ):
        await EmailService.send_email(
            recipients=[email],
            subject="Order Confirmation",
            template_name="order_confirmation.html",
            context={
                "username": username,
                "order_number": order_number,
                "subtotal": subtotal,
                "tax": tax,
                "shipping_charge": shipping_charge,
                "discount": discount,
                "grand_total": grand_total,
            },
        )

    @staticmethod
    async def send_payment_success(
        email: str,
        username: str,
        payment_reference: str,
        order_number: str,
        amount,
        payment_method: str,
    ):
        await EmailService.send_email(
            recipients=[email],
            subject="Payment Successful",
            template_name="payment_success.html",
            context={
                "username": username,
                "payment_reference": payment_reference,
                "order_number": order_number,
                "amount": amount,
                "payment_method": payment_method,
            },
        )
