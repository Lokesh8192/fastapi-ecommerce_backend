from starlette import status

from app.core.error_codes import ErrorCode


class AppException(Exception):
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        status_code: int,
        errors: list | None = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.errors = errors
        super().__init__(message)


class BadRequestException(AppException):
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.VALIDATION_ERROR,
        errors: list | None = None,
    ):
        super().__init__(message, error_code, status.HTTP_400_BAD_REQUEST, errors)


class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Authentication required.",
        error_code: ErrorCode = ErrorCode.INVALID_CREDENTIALS,
    ):
        super().__init__(message, error_code, status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "Permission denied.",
        error_code: ErrorCode = ErrorCode.ACCESS_DENIED,
    ):
        super().__init__(message, error_code, status.HTTP_403_FORBIDDEN)


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found.",
        error_code: ErrorCode = ErrorCode.VALIDATION_ERROR,
    ):
        super().__init__(message, error_code, status.HTTP_404_NOT_FOUND)


class ConflictException(AppException):
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.VALIDATION_ERROR,
    ):
        super().__init__(message, error_code, status.HTTP_409_CONFLICT)