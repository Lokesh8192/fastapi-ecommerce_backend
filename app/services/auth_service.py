from datetime import datetime, timedelta, UTC
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import RefreshTokenRequest, Token


class AuthService:
    def register_user(self, db: Session, user_data: UserCreate) -> UserResponse:
        if UserRepository.get_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        if UserRepository.get_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already Exists",
            )

        user = User(
            username=user_data.username,
            email=user_data.email,
            phone_number=user_data.phone_number,
            hashed_password=hash_password(user_data.password),
        )

        user = UserRepository.create(db, user)

        return UserResponse.model_validate(user)

    def login_user(self, db: Session, login_data: LoginRequest) -> Token:
        user = UserRepository.get_by_email(db, login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

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

        refresh = RefreshToken(
            token=refresh_token,
            user_id=user.id,
            expires_at=datetime.now(UTC)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        RefreshTokenRepository.create(db, refresh)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        payload = decode_token(request.refresh_token)

        if payload["type"] != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        user = UserRepository.get_by_id(
            db,
            int(payload["sub"]),
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )

        return Token(
            access_token=access_token,
            refresh_token=request.refresh_token,
        )

    def logout_user(self, db: Session, refresh_token: str):
        stored_token = RefreshTokenRepository.get_token(
            db,
            refresh_token,
        )

        if stored_token:
            RefreshTokenRepository.delete(db, stored_token)

        return {"message": "Logout successful"}


auth_service = AuthService()

