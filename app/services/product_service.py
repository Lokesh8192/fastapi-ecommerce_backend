from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


class ProductService:
    @staticmethod
    def _get_existing_product(
        db: Session,
        product_id: int,
    ) -> Product:

        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        return product

    @staticmethod
    def create_product(
        db: Session,
        request: ProductCreate,
        current_admin: User,
    ) -> ProductResponse:

        category = CategoryRepository.get_by_id(
            db,
            request.category_id,
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found.",
            )

        if not category.is_active:
            raise HTTPException(
                status_code=400,
                detail="Category is inactive.",
            )

        existing_product = (
            ProductRepository.get_by_name_and_category(
                db,
                request.name,
                request.category_id,
            )
        )

        if existing_product:
            raise HTTPException(
                status_code=400,
                detail="Product already exists in this category.",
            )

        product = Product(
            name=request.name,
            description=request.description,
            price=request.price,
            stock=request.stock,
            image_url=request.image_url,
            category_id=request.category_id,
            created_by=current_admin.id,
        )

        created_product = ProductRepository.create(
            db,
            product,
        )

        return ProductResponse.model_validate(
            created_product
        )

    @staticmethod
    def get_all_products(db: Session):
        products = ProductRepository.get_all(db)

        return [
            ProductResponse.model_validate(product)
            for product in products
        ]

    @staticmethod
    def get_product_by_id(
        db: Session,
        product_id: int,
    ):
        product = ProductService._get_existing_product(
            db,
            product_id,
        )

        return ProductResponse.model_validate(product)

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        request: ProductUpdate,
    ):
        product = ProductService._get_existing_product(
            db,
            product_id,
        )

        product.name = request.name
        product.description = request.description
        product.price = request.price
        product.stock = request.stock
        product.image_url = request.image_url
        product.category_id = request.category_id

        updated_product = ProductRepository.update(
            db,
            product,
        )

        return ProductResponse.model_validate(updated_product)

    @staticmethod
    def activate_product(
        db: Session,
        product_id: int,
    ):
        product = ProductService._get_existing_product(
            db,
            product_id,
        )

        product.is_active = True

        updated_product = ProductRepository.update(
            db,
            product,
        )

        return ProductResponse.model_validate(
            updated_product,
        )

    @staticmethod
    def deactivate_product(
        db: Session,
        product_id: int,
    ):
        product = ProductService._get_existing_product(
            db,
            product_id,
        )

        product.is_active = False

        updated_product = ProductRepository.update(
            db,
            product,
        )

        return ProductResponse.model_validate(
            updated_product,
        )


product_service = ProductService()
