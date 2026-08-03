from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
)
from app.models.enums import OrderStatus
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import (
    OrderCreate,
    OrderItemResponse,
    OrderResponse,
    OrderSummaryResponse,
    OrderStatus,
)
from app.schemas.adress import AddressResponse
from app.services.address_service import address_service
from app.utils.order_number import generate_order_number


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
    ):
        self.order_repository = order_repository
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    @staticmethod
    def _to_response(order: Order) -> OrderResponse:
        return OrderResponse(
            order_id=order.id,
            order_number=order.order_number,
            address_id=order.address_id,
            status=order.status,
            subtotal=order.subtotal,
            tax=order.tax,
            shipping_charge=order.shipping_charge,
            discount=order.discount,
            grand_total=order.grand_total,
            created_at=order.created_at,
            address=AddressResponse.model_validate(order.address),
            items=[
                OrderItemResponse(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.total_price,
                )
                for item in order.items
            ],
        )

    @staticmethod
    def _to_summary(order: Order) -> OrderSummaryResponse:
        return OrderSummaryResponse(
            order_id=order.id,
            order_number=order.order_number,
            status=order.status,
            grand_total=order.grand_total,
            created_at=order.created_at,
        )

    def create_order(
        self,
        db: Session,
        user_id: int,
        request: OrderCreate,
        tax: Decimal = Decimal("0"),
        shipping_charge: Decimal = Decimal("0"),
        discount: Decimal = Decimal("0"),
    ) -> OrderResponse:
        """
        Create an order from the user's cart.
        """

        if min(tax, shipping_charge, discount) < 0:
            raise BadRequestException(
                "Order charges and discount cannot be negative."
            )

        cart = self.cart_repository.get_cart_by_user_id(
            db,
            user_id,
        )

        if not cart or not cart.items:
            raise BadRequestException("Cart is empty.")

        try:
            address = address_service._get_user_address(
                db=db,
                user_id=user_id,
                address_id=request.address_id,
            )

            subtotal = Decimal("0")
            products = []

            for cart_item in cart.items:
                product = self.product_repository.get_by_id(
                    db,
                    cart_item.product_id,
                )

                if not product or not product.is_active:
                    raise BadRequestException(
                        f"Product with id {cart_item.product_id} is unavailable."
                    )

                if cart_item.quantity > product.stock_quantity:
                    raise BadRequestException(
                        f"Insufficient stock for product '{product.name}'."
                    )

                products.append((cart_item, product))
                subtotal += product.price * cart_item.quantity

            grand_total = (
                subtotal
                + tax
                + shipping_charge
                - discount
            )

            if grand_total < 0:
                raise BadRequestException(
                    "Discount cannot exceed the order total."
                )

            order = self.order_repository.create_order(
                db,
                Order(
                    order_number=generate_order_number(),
                    user_id=user_id,
                    address_id=address.id,
                    status=OrderStatus.PENDING,
                    subtotal=subtotal,
                    tax=tax,
                    shipping_charge=shipping_charge,
                    discount=discount,
                    grand_total=grand_total,
                ),
            )

            for cart_item, product in products:
                line_total = (
                    product.price
                    * cart_item.quantity
                )

                self.order_repository.create_order_item(
                    db,
                    OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        product_name=product.name,
                        quantity=cart_item.quantity,
                        unit_price=product.price,
                        total_price=line_total,
                    ),
                )

                product.stock_quantity -= cart_item.quantity

            self.cart_repository.clear_cart(
                db,
                cart.id,
            )

            db.commit()
            db.refresh(order)

        except Exception:
            db.rollback()
            raise

        return self.get_order_by_id(
            db,
            user_id,
            order.id,
        )

    def get_order_by_id(
        self,
        db: Session,
        user_id: int,
        order_id: int,
    ) -> OrderResponse:

        order = self.order_repository.get_order_by_id(
            db,
            order_id,
        )

        if not order or order.user_id != user_id:
            raise NotFoundException("Order not found.")

        return self._to_response(order)

    def get_orders(
        self,
        db: Session,
        user_id: int,
    ) -> list[OrderSummaryResponse]:

        orders = self.order_repository.get_order_by_user(
            db,
            user_id,
        )

        return [
            self._to_summary(order)
            for order in orders
        ]

    def update_order_status(
        self,
        db: Session,
        order_id: int,
        status: OrderStatus,
    ) -> OrderResponse:

        order = self.order_repository.get_order_by_id(
            db,
            order_id,
        )

        if not order:
            raise NotFoundException("Order not found.")

        allowed_transitions = {
            OrderStatus.PENDING: {
                OrderStatus.CONFIRMED,
                OrderStatus.CANCELLED,
            },
            OrderStatus.CONFIRMED: {
                OrderStatus.SHIPPED,
                OrderStatus.CANCELLED,
            },
            OrderStatus.SHIPPED: {
                OrderStatus.DELIVERED,
            },
            OrderStatus.DELIVERED: {
                OrderStatus.RETURNED,
            },
            OrderStatus.RETURNED: set(),
            OrderStatus.CANCELLED: set(),
        }

        if status == order.status:
            raise BadRequestException(
                f"Order is already in '{status.value}' status."
            )

        if status not in allowed_transitions.get(order.status, set()):
            raise BadRequestException(
                f"Cannot change order status from "
                f"'{order.status.value}' to '{status.value}'."
            )

        try:
            order.status = status

            self.order_repository.update_order(
                db,
                order,
            )

            db.commit()
            db.refresh(order)

        except Exception:
            db.rollback()
            raise

        return self._to_response(order)


order_service = OrderService(
    OrderRepository(),
    CartRepository(),
    ProductRepository(),
)
