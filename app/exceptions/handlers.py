import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.error_codes import ErrorCode
from app.exceptions.custom_exceptions import AppException


logger = logging.getLogger(__name__)


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": exc.error_code.value,
            "message": exc.message,
            "errors": exc.errors,
            "request_id": _request_id(request),
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = [
        {
            "field": ".".join(map(str, error["loc"][1:])),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error_code": ErrorCode.VALIDATION_ERROR.value,
            "message": "Validation failed.",
            "errors": errors,
            "request_id": _request_id(request),
        },
    )


async def internal_server_error_handler(
    request: Request,
    exc: Exception,
):
    request_id = _request_id(request)
    logger.exception(
        "request_id=%s path=%s error=%s",
        request_id,
        request.url.path,
        str(exc),
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": ErrorCode.INTERNAL_SERVER_ERROR.value,
            "message": "Internal server error.",
            "errors": None,
            "request_id": request_id,
        },
    )