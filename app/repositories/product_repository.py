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
    def get_all(
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
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        product: Product,
    ) -> Product:
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_all_by_dmin(
        db: Session,
    ) -> list[Product]:
        return (
            db.query(Product)
            .order_by(Product.id)
            .all()
        )
