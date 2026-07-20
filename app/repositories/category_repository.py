from sqlalchemy.orm import Session
from app.models.category import Category


class CategoryRepository:
    @staticmethod
    def create(
        db: Session,
        category: Category,
    ) -> Category:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Category]:
        return (
            db.query(Category)
            .filter(Category.is_active == True)
            .order_by(Category.id)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: int,
    ) -> Category | None:
        return (
            db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        name: str,
    ) -> Category | None:
        return (
            db.query(Category)
            .filter(Category.name == name)
            .first()
        )

    @staticmethod
    def get_by_names(
        db: Session,
        names: list[str],
    ) -> list[Category]:
        return (
            db.query(Category)
            .filter(Category.name.in_(names))
            .all()
        )

    @staticmethod
    def create_many(
        db: Session,
        categories: list[Category],
    ) -> list[Category]:
        try:
            db.add_all(categories)
            db.commit()
        except Exception:
            db.rollback()
            raise

        for category in categories:
            db.refresh(category)

        return categories

    @staticmethod
    def update(
        db: Session,
        category: Category,
    ) -> Category:
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete(
        db: Session,
        category: Category,
    ) -> None:
        category.is_active = False
        CategoryRepository.update(db, category)
        db.commit()

