from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.error_codes import ErrorCode
from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from app.models.product import Product
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.cache_service import CacheService


class ProductService:

    @staticmethod
    def _get_existing_product(
        db: Session,
        product_id: int,
    ) -> Product:
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise NotFoundException(
                "Product not found.",
                ErrorCode.PRODUCT_NOT_FOUND,
            )

        return product

    @staticmethod
    def _get_active_category(
        db: Session,
        category_id: int,
    ):
        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise NotFoundException(
                "Category not found.",
                ErrorCode.CATEGORY_NOT_FOUND,
            )

        if not category.is_active:
            raise BadRequestException(
                "Category is inactive.",
                ErrorCode.CATEGORY_INACTIVE,
            )

        return category

    @staticmethod
    def create_product(
        db: Session,
        request: ProductCreate,
        current_admin: User,
    ) -> ProductResponse:

        ProductService._get_active_category(
            db,
            request.category_id,
        )

        if ProductRepository.get_by_name_and_category(
            db,
            request.name,
            request.category_id,
        ):
            raise ConflictException(
                "Product already exists in this category.",
                ErrorCode.PRODUCT_ALREADY_EXISTS,
            )

        product = Product(
            name=request.name,
            description=request.description,
            price=request.price,
            stock_quantity=request.stock_quantity,
            image_url=request.image_url,
            category_id=request.category_id,
            created_by=current_admin.id,
        )

        created_product = ProductRepository.create(
            db,
            product,
        )

        CacheService.clear()

        return ProductResponse.model_validate(created_product)

    @staticmethod
    def get_all_products(
        db: Session,
    ) -> list[ProductResponse]:

        products = ProductRepository.get_all_active(db)

        return [
            ProductResponse.model_validate(product)
            for product in products
        ]

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
    ) -> list[ProductResponse]:

        if page < 1:
            raise BadRequestException(
                "Page must be greater than 0.",
                ErrorCode.INVALID_PAGE,
            )

        if size < 1 or size > 100:
            raise BadRequestException(
                "Page size must be between 1 and 100.",
                ErrorCode.INVALID_PAGE_SIZE,
            )

        if (
            min_price is not None
            and max_price is not None
            and min_price > max_price
        ):
            raise BadRequestException(
                "Minimum price cannot be greater than maximum price.",
                ErrorCode.INVALID_PRICE_RANGE,
            )

        if sort_by not in {
            "name",
            "price",
            "created_at",
        }:
            raise BadRequestException(
                "Invalid sort field.",
                ErrorCode.INVALID_SORT_FIELD,
            )

        if order.lower() not in {
            "asc",
            "desc",
        }:
            raise BadRequestException(
                "Order must be asc or desc.",
                ErrorCode.INVALID_SORT_FIELD,
            )

        if category_id is not None:
            ProductService._get_active_category(
                db,
                category_id,
            )

        cache_key = (
            f"products:{search}:{category_id}:{min_price}:{max_price}:"
            f"{sort_by}:{order}:{page}:{size}"
        )

        cached_products = CacheService.get(cache_key)

        if cached_products:
            return [
                ProductResponse.model_validate(product)
                for product in cached_products
            ]

        products = ProductRepository.get_products(
            db,
            search,
            category_id,
            min_price,
            max_price,
            sort_by,
            order,
            page,
            size,
        )

        response = [
            ProductResponse.model_validate(product).model_dump(
                mode="json"
            )
            for product in products
        ]

        CacheService.set(
            cache_key,
            response,
        )

        return [
            ProductResponse.model_validate(product)
            for product in response
        ]

    @staticmethod
    def get_product_by_id(
        db: Session,
        product_id: int,
    ) -> ProductResponse:

        product = ProductService._get_existing_product(
            db,
            product_id,
        )

        if not product.is_active:
            raise NotFoundException(
                "Product not found.",
                ErrorCode.PRODUCT_NOT_FOUND,
            )

        return ProductResponse.model_validate(product)

    @staticmethod
    def update_product_status(
        db: Session,
        product_id: int,
        is_active: bool,
    ) -> ProductResponse:

        product = ProductService._get_existing_product(
            db,
            product_id,
        )

        product.is_active = is_active

        updated_product = ProductRepository.update(
            db,
            product,
        )

        CacheService.clear()

        return ProductResponse.model_validate(updated_product)

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        request: ProductUpdate,
    ) -> ProductResponse:

        product = ProductService._get_existing_product(
            db,
            product_id,
        )

        if request.category_id is not None:
            ProductService._get_active_category(
                db,
                request.category_id,
            )
            product.category_id = request.category_id

        if request.name is not None:
            category_id = (
                request.category_id
                if request.category_id is not None
                else product.category_id
            )

            existing_product = ProductRepository.get_by_name_and_category(
                db,
                request.name,
                category_id,
            )

            if (
                existing_product
                and existing_product.id != product.id
            ):
                raise ConflictException(
                    "Product already exists in this category.",
                    ErrorCode.PRODUCT_ALREADY_EXISTS,
                )

            product.name = request.name

        for field in (
            "description",
            "price",
            "stock_quantity",
            "image_url",
            "is_active",
        ):
            value = getattr(request, field)

            if value is not None:
                setattr(
                    product,
                    field,
                    value,
                )

        updated_product = ProductRepository.update(
            db,
            product,
        )

        CacheService.clear()

        return ProductResponse.model_validate(updated_product)

    @staticmethod
    def update_stock_quantity(
        db: Session,
        product_id: int,
        stock_quantity: int,
    ) -> ProductResponse:

        product = ProductService._get_existing_product(
            db,
            product_id,
        )

        product.stock_quantity = stock_quantity

        updated_product = ProductRepository.update(
            db,
            product,
        )

        CacheService.clear()

        return ProductResponse.model_validate(updated_product)

    @staticmethod
    def validate_stock(
        product: Product,
        quantity: int,
    ) -> None:

        if not product.is_active:
            raise BadRequestException(
                "Product is inactive.",
                ErrorCode.PRODUCT_INACTIVE,
            )

        if product.stock_quantity < quantity:
            raise BadRequestException(
                "Insufficient stock available.",
                ErrorCode.INSUFFICIENT_STOCK,
            )

    @staticmethod
    def deduct_stock(
        db: Session,
        product: Product,
        quantity: int,
    ) -> None:

        product.stock_quantity -= quantity

        ProductRepository.update(
            db,
            product,
        )

        CacheService.clear()

    @staticmethod
    def restore_stock(
        db: Session,
        product: Product,
        quantity: int,
    ) -> None:

        product.stock_quantity += quantity

        ProductRepository.update(
            db,
            product,
        )

        CacheService.clear()

    @staticmethod
    def get_low_stock_products(
        db: Session,
        threshold: int = 10,
    ) -> list[ProductResponse]:

        products = ProductRepository.get_low_stock_products(
            db,
            threshold,
        )

        return [
            ProductResponse.model_validate(product)
            for product in products
        ]

    @staticmethod
    def get_out_of_stock_products(
        db: Session,
    ) -> list[ProductResponse]:

        products = ProductRepository.get_out_of_stock_products(db)

        return [
            ProductResponse.model_validate(product)
            for product in products
        ]


product_service = ProductService()