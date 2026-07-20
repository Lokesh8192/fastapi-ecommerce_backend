from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import (
    CategoryBulkCreate,
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)


class CategoryService:

    @staticmethod
    def create_category(
        db: Session,
        request: CategoryCreate,
        current_admin: User,
    ) -> CategoryResponse:

        existing_category = CategoryRepository.get_by_name(
            db,
            request.name,
        )

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists.",
            )

        category = Category(
            name=request.name,
            description=request.description,
            created_by=current_admin.id,
        )

        created_category = CategoryRepository.create(
            db,
            category,
        )

        return CategoryResponse.model_validate(
            created_category,
        )

    @staticmethod
    def create_categories(
        db: Session,
        request: CategoryBulkCreate,
        current_admin: User,
    ) -> list[CategoryResponse]:
        names = [category.name for category in request.categories]
        existing_categories = CategoryRepository.get_by_names(db, names)

        if existing_categories:
            existing_names = ", ".join(
                category.name for category in existing_categories
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Categories already exist: "
                    f"{existing_names}. No categories were created."
                ),
            )

        categories = [
            Category(
                name=category.name,
                description=category.description,
                created_by=current_admin.id,
            )
            for category in request.categories
        ]
        created_categories = CategoryRepository.create_many(db, categories)

        return [
            CategoryResponse.model_validate(category)
            for category in created_categories
        ]

    @staticmethod
    def get_all_categories(
        db: Session,
    ):

        categories = CategoryRepository.get_all(db)

        return [
            CategoryResponse.model_validate(category)
            for category in categories
        ]

    @staticmethod
    def get_category_by_id(
        db: Session,
        category_id: int,
    ):

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return CategoryResponse.model_validate(category)

    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        request: CategoryUpdate,
    ):

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        if request.name:

            existing_category = CategoryRepository.get_by_name(
                db,
                request.name,
            )

            if (
                existing_category
                and existing_category.id != category.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category already exists.",
                )

            category.name = request.name

        if request.description is not None:
            category.description = request.description

        updated_category = CategoryRepository.update(
            db,
            category,
        )

        return CategoryResponse.model_validate(
            updated_category,
        )

    @staticmethod
    def activate_category(
        db: Session,
        category_id: int,
    ):

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        category.is_active = True

        updated_category = CategoryRepository.update(
            db,
            category,
        )

        return CategoryResponse.model_validate(
            updated_category,
        )

    @staticmethod
    def deactivate_category(
        db: Session,
        category_id: int,
    ):

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        category.is_active = False

        updated_category = CategoryRepository.update(
            db,
            category,
        )

        return CategoryResponse.model_validate(
            updated_category,
        )

    @staticmethod
    def _get_existing_category(
        db: Session,
        category_id: int,
    ) -> Category:

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return category


category_service = CategoryService()

