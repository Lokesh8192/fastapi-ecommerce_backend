from fastapi import FastAPI
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.admin import router as admin_router
from app.api.category import router as category_router
from app.api.product import router as product_router



app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(category_router)
app.include_router(product_router)

@app.get("/")
def home():
    return {
        "message": "E-commerce backed API Running Successfully"
    }


@app.get("/health")
def Health():
    return {
        "status": "healthy"
    }
