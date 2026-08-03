from sqlalchemy.orm import Session, joinedload
from app.models.order import Order
from app.models.order_item import OrderItem


class OrderRepository:
    def create_order(self, db: Session, order: Order,) -> Order:
        db.add(order)
        db.flush()
        db.refresh(order)

        return order

    def create_order_item(self, db: Session, order_item: OrderItem,) -> OrderItem:
        db.add(order_item)
        db.flush()
        db.refresh(order_item)

        return order_item

    def get_order_by_id(
        self,
        db: Session,
        order_id: int,
    ) -> Order | None:
        return (
            db.query(Order)
            .options(
                joinedload(Order.items),
                joinedload(Order.address),
                joinedload(Order.user),
            )
            .filter(Order.id == order_id)
            .first()
        )

    def get_order_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Order]:
        return (
            db.query(Order)
            .options(
                joinedload(Order.items),
                joinedload(Order.address),
                joinedload(Order.user),
            )
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    def update_order(self, db: Session, order: Order) -> Order:
        db.flush()
        db.refresh(order)

        return order
