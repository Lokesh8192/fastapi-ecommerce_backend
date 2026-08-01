from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.error_codes import ErrorCode
from app.exceptions.custom_exceptions import BadRequestException, NotFoundException
from app.models.cart_item import CartItem
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import (
    AddToCartRequest,
    CartItemResponse,
    CartResponse,
    UpdateCartItemRequest,
)


class CartService:
    def __init__(
        self,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
    ):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def _get_or_create_cart(self, db: Session, user_id: int):
        cart = self.cart_repository.get_cart_by_user_id(db, user_id)
        if cart:
            return cart
        return self.cart_repository.create_cart(db, user_id)

    @staticmethod
    def _to_response(cart) -> CartResponse:
        items = [
            CartItemResponse(
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.price_at_added,
                total_price=item.price_at_added * item.quantity,
            )
            for item in cart.items
        ]
        return CartResponse(
            cart_id=cart.id,
            total_items=sum(item.quantity for item in cart.items),
            subtotal=sum((item.total_price for item in items), Decimal("0")),
            items=items,
        )

    def _get_cart_response(self, db: Session, user_id: int) -> CartResponse:
        cart = self.cart_repository.get_cart_by_user_id(db, user_id)
        if not cart:
            return CartResponse(
                cart_id=0,
                total_items=0,
                subtotal=Decimal("0"),
                items=[],
            )
        return self._to_response(cart)

    def add_to_cart(
        self,
        db: Session,
        user_id: int,
        request: AddToCartRequest,
    ) -> CartResponse:
        product = self.product_repository.get_by_id(db, request.product_id)
        if not product or not product.is_active:
            raise NotFoundException("Product not found.", ErrorCode.PRODUCT_NOT_FOUND)
        if request.quantity > product.stock_quantity:
            raise BadRequestException("Insufficient stock.")

        try:
            cart = self._get_or_create_cart(db, user_id)
            cart_item = self.cart_repository.get_cart_item(db, cart.id, product.id)
            if cart_item:
                new_quantity = cart_item.quantity + request.quantity
                if new_quantity > product.stock_quantity:
                    raise BadRequestException("Insufficient stock.")
                cart_item.quantity = new_quantity
                self.cart_repository.update_cart_item(db, cart_item)
            else:
                self.cart_repository.add_cart_item(
                    db,
                    CartItem(
                        cart_id=cart.id,
                        product_id=product.id,
                        quantity=request.quantity,
                        price_at_added=product.price,
                    ),
                )
            db.commit()
        except Exception:
            db.rollback()
            raise

        return self._get_cart_response(db, user_id)

    def get_cart(self, db: Session, user_id: int) -> CartResponse:
        return self._get_cart_response(db, user_id)

    def update_item(
        self,
        db: Session,
        user_id: int,
        product_id: int,
        request: UpdateCartItemRequest,
    ) -> CartResponse:
        cart_item = self.cart_repository.get_cart_item_by_user_id(
            db,
            user_id,
            product_id,
        )
        if not cart_item:
            raise NotFoundException("Cart item not found.")
        product = self.product_repository.get_by_id(db, product_id)
        if not product or not product.is_active:
            raise NotFoundException("Product not found.", ErrorCode.PRODUCT_NOT_FOUND)
        if request.quantity > product.stock_quantity:
            raise BadRequestException("Insufficient stock.")

        try:
            cart_item.quantity = request.quantity
            self.cart_repository.update_cart_item(db, cart_item)
            db.commit()
        except Exception:
            db.rollback()
            raise
        return self._get_cart_response(db, user_id)

    def remove_item(self, db: Session, user_id: int, product_id: int) -> CartResponse:
        cart_item = self.cart_repository.get_cart_item_by_user_id(
            db,
            user_id,
            product_id,
        )
        if not cart_item:
            raise NotFoundException("Cart item not found.")
        try:
            self.cart_repository.remove_cart_item(db, cart_item)
            db.commit()
        except Exception:
            db.rollback()
            raise
        return self._get_cart_response(db, user_id)

    def clear_cart(self, db: Session, user_id: int) -> None:
        cart = self.cart_repository.get_cart_by_user_id(db, user_id)
        if not cart:
            return
        try:
            self.cart_repository.clear_cart(db, cart.id)
            db.commit()
        except Exception:
            db.rollback()
            raise


cart_service = CartService(CartRepository(), ProductRepository())
