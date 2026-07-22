from decimal import Decimal
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:

    @staticmethod
    def create(
        db: Session,
        product: Product,
    ) -> Product:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_all_active(
        db: Session,
    ) -> list[Product]:
        return (
            db.query(Product)
            .filter(Product.is_active.is_(True))
            .order_by(Product.id)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: int,
    ) -> Product | None:
        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    @staticmethod
    def get_by_name_and_category(
        db: Session,
        name: str,
        category_id: int,
    ) -> Product | None:
        return (
            db.query(Product)
            .filter(
                Product.name == name,
                Product.category_id == category_id,
                Product.is_active.is_(True),
            )
            .first()
        )

    @staticmethod
    def get_products(
        db: Session,
        search: str | None = None,
        category_id: int | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
        page: int = 1,
        size: int = 10,
    ) -> list[Product]:

        query = (
            db.query(Product)
            .filter(Product.is_active.is_(True))
        )

        # Search
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                )
            )

        # Category
        if category_id is not None:
            query = query.filter(
                Product.category_id == category_id
            )

        # Minimum Price
        if min_price is not None:
            query = query.filter(
                Product.price >= min_price
            )

        # Maximum Price
        if max_price is not None:
            query = query.filter(
                Product.price <= max_price
            )

        # Sorting
        sortable_columns = {
            "name": Product.name,
            "price": Product.price,
            "created_at": Product.created_at,
        }

        column = sortable_columns.get(
            sort_by,
            Product.created_at,
        )

        if order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

        # Pagination
        offset = (page - 1) * size

        query = (
            query.offset(offset)
            .limit(size)
        )

        return query.all()

    @staticmethod
    def update(
        db: Session,
        product: Product,
    ) -> Product:
        db.commit()
        db.refresh(product)
        return product
