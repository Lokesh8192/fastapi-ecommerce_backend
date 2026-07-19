from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.roles import UserRole
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    ChangePasswordRequest,
    UserResponse,
    UserRoleUpdate,
    UserUpdate,
)


class UserService:
    @staticmethod
    def update_profile(
        db: Session,
        current_user: User,
        request: UserUpdate,
    ) -> UserResponse:
        if request.username:
            existing_user = UserRepository.get_by_username(
                db,
                request.username,
            )
            if existing_user and existing_user.id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists.",
                )
            current_user.username = request.username

        if request.phone_number:
            current_user.phone_number = request.phone_number

        updated_user = UserRepository.update(db, current_user)
        return UserResponse.model_validate(updated_user)

    @staticmethod
    def change_password(
        db: Session,
        current_user: User,
        request: ChangePasswordRequest,
    ):
        if not verify_password(request.old_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect.",
            )

        if request.old_password == request.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from the old password.",
            )

        current_user.hashed_password = hash_password(request.new_password)
        UserRepository.update(db, current_user)
        RefreshTokenRepository.delete_by_user(db, current_user.id)

        return {"message": "Password changed successfully."}

    @staticmethod
    def deactivate_account(db: Session, current_user: User):
        current_user.is_active = False
        UserRepository.update(db, current_user)
        RefreshTokenRepository.delete_by_user(db, current_user.id)

        return {"message": "Account deactivated successfully."}

    @staticmethod
    def get_all_users(db: Session) -> list[UserResponse]:
        users = db.query(User).order_by(User.id).all()
        return [UserResponse.model_validate(user) for user in users]

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> UserResponse:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return UserResponse.model_validate(user)

    @staticmethod
    def update_role(
        db: Session,
        current_admin: User,
        user_id: int,
        request: UserRoleUpdate,
    ) -> UserResponse:
        if current_admin.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot change your own role.",
            )

        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        user.role = request.role.value if isinstance(
            request.role, UserRole) else request.role
        updated_user = UserRepository.update(db, user)
        return UserResponse.model_validate(updated_user)

    @staticmethod
    def activate_user(db: Session, user_id: int) -> UserResponse:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        user.is_active = True
        updated_user = UserRepository.update(db, user)
        return UserResponse.model_validate(updated_user)

    @staticmethod
    def deactivate_user(
        db: Session,
        current_admin: User,
        user_id: int,
    ) -> UserResponse:
        if current_admin.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot deactivate your own account.",
            )

        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        user.is_active = False
        updated_user = UserRepository.update(db, user)
        RefreshTokenRepository.delete_by_user(db, user.id)
        return UserResponse.model_validate(updated_user)


user_service = UserService()
