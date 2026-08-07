from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.error_codes import ErrorCode
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.exceptions.custom_exceptions import (
    ConflictException,
    UnauthorizedException,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.schemas.token import RefreshTokenRequest, Token
from app.schemas.user import UserCreate, UserResponse


class AuthService:

    def register_user(
        self,
        db: Session,
        user_data: UserCreate,
    ) -> UserResponse:

        if UserRepository.get_by_email(db, user_data.email):
            raise ConflictException(
                "Email already registered.",
                ErrorCode.USER_ALREADY_EXISTS,
            )

        if UserRepository.get_by_username(db, user_data.username):
            raise ConflictException(
                "Username already exists.",
                ErrorCode.USER_ALREADY_EXISTS,
            )

        user = User(
            username=user_data.username,
            email=user_data.email,
            phone_number=user_data.phone_number,
            hashed_password=hash_password(user_data.password),
            role=(user_data.role if getattr(user_data, "role", None) else "customer"),
        )

        created_user = UserRepository.create(db, user)

        return UserResponse.model_validate(created_user)

    def login_user(
        self,
        db: Session,
        login_data: LoginRequest,
    ) -> Token:

        user = UserRepository.get_by_email(
            db,
            login_data.email,
        )

        if (
            not user
            or not verify_password(
                login_data.password,
                user.hashed_password,
            )
        ):
            raise UnauthorizedException(
                "Invalid email or password.",
                ErrorCode.INVALID_CREDENTIALS,
            )

        return self._create_tokens(
            db,
            user,
        )

    def refresh_access_token(
        self,
        db: Session,
        request: RefreshTokenRequest,
    ) -> Token:

        stored_token = RefreshTokenRepository.get_token(
            db,
            request.refresh_token,
        )

        if not stored_token:
            raise UnauthorizedException(
                "Invalid refresh token.",
                ErrorCode.INVALID_TOKEN,
            )

        payload = decode_token(request.refresh_token)

        if payload.get("type") != "refresh":
            raise UnauthorizedException(
                "Invalid token type.",
                ErrorCode.INVALID_TOKEN,
            )

        user = UserRepository.get_by_id(
            db,
            int(payload["sub"]),
        )

        if not user:
            raise UnauthorizedException(
                "Invalid refresh token.",
                ErrorCode.INVALID_TOKEN,
            )

        return Token(
            access_token=create_access_token(
                {
                    "sub": str(user.id),
                    "email": user.email,
                    "role": user.role,
                }
            ),
            refresh_token=request.refresh_token,
        )

    def logout_user(
        self,
        db: Session,
        refresh_token: str,
    ):

        stored_token = RefreshTokenRepository.get_token(
            db,
            refresh_token,
        )

        if stored_token:
            RefreshTokenRepository.delete(
                db,
                stored_token,
            )

        return {"message": "Logout successful."}

    def _create_tokens(
        self,
        db: Session,
        user: User,
    ) -> Token:

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
            }
        )

        RefreshTokenRepository.create(
            db,
            RefreshToken(
                token=refresh_token,
                user_id=user.id,
                expires_at=datetime.now(UTC)
                + timedelta(
                    days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
                ),
            ),
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )


auth_service = AuthService()
