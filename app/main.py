from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.category import router as category_router
from app.api.product import router as product_router
from app.api.user import router as user_router
from app.core.config import settings
from app.exceptions.custom_exceptions import AppException
from app.exceptions.handlers import (
    app_exception_handler,
    internal_server_error_handler,
    validation_exception_handler,
)
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.request_context import RequestContextMiddleware
from app.api.cart import router as cart_router
from app.api.order import router as order_router
from app.api.payment import router as payment_router
from app.api.address import router as address_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, internal_server_error_handler)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestContextMiddleware)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(address_router)
app.include_router(admin_router)
app.include_router(category_router)
# app.include_router(
#     category_router,
#     prefix="/api",
# )
app.include_router(product_router)
app.include_router(
    cart_router,
    prefix="/api/v1",
)
app.include_router(
    order_router,
    prefix="/api/v1",
)
app.include_router(
    payment_router,
    prefix="/api/v1",
)


@app.get("/")
def home():
    return {"message": "E-commerce backend API running successfully."}


@app.get("/health")
def health():
    return {"status": "healthy"}
