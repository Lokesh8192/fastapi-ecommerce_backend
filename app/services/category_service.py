from sqlalchemy.orm import Session

from app.core.error_codes import ErrorCode
from app.exceptions.custom_exceptions import ConflictException, NotFoundException
from app.models.category import Category
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryBulkCreate, CategoryCreate, CategoryResponse, CategoryUpdate


class CategoryService:
    @staticmethod
    def _get_existing_category(db: Session, category_id: int) -> Category:
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise NotFoundException(
                "Category not found.", ErrorCode.CATEGORY_NOT_FOUND)
        return category

    @staticmethod
    def create_category(db: Session, request: CategoryCreate, current_admin: User) -> CategoryResponse:
        if CategoryRepository.get_by_name(db, request.name):
            raise ConflictException(
                "Category already exists.", ErrorCode.CATEGORY_ALREADY_EXISTS)
        category = Category(
            name=request.name, description=request.description, created_by=current_admin.id)
        return CategoryResponse.model_validate(CategoryRepository.create(db, category))

    @staticmethod
    def create_categories(db: Session, request: CategoryBulkCreate, current_admin: User) -> list[CategoryResponse]:
        names = [category.name for category in request.categories]
        existing_categories = CategoryRepository.get_by_names(db, names)
        if existing_categories:
            existing_names = ", ".join(
                category.name for category in existing_categories)
            raise ConflictException(
                f"Categories already exist: {existing_names}. No categories were created.",
                ErrorCode.CATEGORY_ALREADY_EXISTS,
            )
        categories = [Category(name=item.name, description=item.description,
                               created_by=current_admin.id) for item in request.categories]
        return [CategoryResponse.model_validate(category) for category in CategoryRepository.create_many(db, categories)]

    @staticmethod
    def get_all_categories(db: Session) -> list[CategoryResponse]:
        return [CategoryResponse.model_validate(category) for category in CategoryRepository.get_all(db)]

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> CategoryResponse:
        return CategoryResponse.model_validate(CategoryService._get_existing_category(db, category_id))

    @staticmethod
    def update_category(db: Session, category_id: int, request: CategoryUpdate) -> CategoryResponse:
        category = CategoryService._get_existing_category(db, category_id)
        if request.name is not None:
            existing_category = CategoryRepository.get_by_name(
                db, request.name)
            if existing_category and existing_category.id != category.id:
                raise ConflictException(
                    "Category already exists.", ErrorCode.CATEGORY_ALREADY_EXISTS)
            category.name = request.name
        if request.description is not None:
            category.description = request.description
        return CategoryResponse.model_validate(CategoryRepository.update(db, category))

    @staticmethod
    def update_category_status(db: Session, category_id: int, is_active: bool) -> CategoryResponse:
        category = CategoryService._get_existing_category(db, category_id)
        category.is_active = is_active
        return CategoryResponse.model_validate(CategoryRepository.update(db, category))


category_service = CategoryService()
