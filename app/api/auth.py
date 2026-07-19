from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.depedencies import get_db
from app.schemas.auth import LoginRequest
from app.schemas.token import RefreshTokenRequest, Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import auth_service
from app.schemas.common import ApiResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authetication"],
)


@router.post(
    "/register",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user: UserCreate, db: Session = Depends(get_db),):
    user_response = auth_service.register_user(db, user)

    return ApiResponse(
        success=True,
        message="User registered successfully.",
        data=user_response,
    )


@router.post("/login", response_model=ApiResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    login = auth_service.login_user(db, login_data)

    return ApiResponse(
        success=True,
        message="Login successful.",
        data=login,
    )


@router.post("/refresh", response_model=ApiResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db),):
    token = auth_service.refresh_access_token(db, request)

    return ApiResponse(
        success=True,
        message="Access token refreshed successfully.",
        data=token,
    )


@router.post("/logout", response_model=ApiResponse)
def logout(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    auth_service.logout_user(db, request.refresh_token)

    return ApiResponse(
        success=True,
        message="Logout successful.",
    )
