from sqlalchemy.orm import Session, joinedload
from app.models.cart import Cart
from app.models.cart_item import CartItem


class CartRepository:
    def create_cart(
        self,
        db: Session,
        user_id: int,
    ) -> Cart:
        cart = Cart(user_id=user_id)

        db.add(cart)
        db.flush()
        db.refresh(cart)

        return cart

    def get_cart_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> Cart | None:
        return (
            db.query(Cart)
            .options(joinedload(Cart.items).joinedload(CartItem.product))
            .filter(Cart.user_id == user_id)
            .first()
        )

    def get_cart_by_id(
        self,
        db: Session,
        cart_id: int,
    ) -> Cart | None:
        return (
            db.query(Cart)
            .filter(Cart.id == cart_id)
            .first()
        )

    def get_cart_item(
        self,
        db: Session,
        cart_id: int,
        product_id: int,
    ) -> CartItem | None:
        return (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
            .first()
        )

    def add_cart_item(
        self,
        db: Session,
        cart_item: CartItem,
    ) -> CartItem:

        db.add(cart_item)

        db.flush()

        db.refresh(cart_item)

        return cart_item

    def update_cart_item(
        self,
        db: Session,
        cart_item: CartItem,
    ) -> CartItem:

        db.flush()

        db.refresh(cart_item)

        return cart_item

    def remove_cart_item(
        self,
        db: Session,
        cart_item: CartItem,
    ):

        db.delete(cart_item)

        db.flush()

    def clear_cart(
        self,
        db: Session,
        cart_id: int,
    ):

        (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id
            )
            .delete()
        )

        db.flush()

