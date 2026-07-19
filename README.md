# E-Commerce Backend API

A FastAPI-based e-commerce backend service for authentication, user management, and admin access.

For a separate, detailed explanation of the main application flow, see [NOTES.md](NOTES.md).

## Project Overview

This project provides a scalable REST API foundation for an e-commerce system. It includes:

- User registration and login
- JWT-based authentication and token refresh
- User profile access
- Admin dashboard access
- SQLAlchemy ORM integration with PostgreSQL
- Environment-based configuration using Pydantic settings

## Tech Stack

- Python 3.x
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT authentication via `python-jose`
- Uvicorn server

## Project Structure

- `app/main.py` — application startup and route registration
- `app/api/` — API endpoints for auth, users, and admin
- `app/core/` — settings, security, and shared dependencies
- `app/db/` — database connection and session management
- `app/models/` — SQLAlchemy models
- `app/schemas/` — request/response schema definitions
- `app/services/` — business logic layer
- `app/repositories/` — database repository layer

## Environment Configuration

Create a `.env` file in the project root with the required configuration values, for example:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecommerce_db
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecommerce_test_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
PROJECT_NAME=E-Commerce Backend API
API_VERSION=v1
DEBUG=False
```

## Installation

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## File Notes

### `app/main.py`

This file is the main application entrypoint. It creates the FastAPI application instance, registers all routers, and defines the root and health-check endpoints.

#### Syntax

```python
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)
```

#### Explanation

- `FastAPI()` initializes the web application.
- `title=settings.PROJECT_NAME` sets the API title from the environment configuration.
- `version=settings.API_VERSION` sets the API version.

#### Router Registration

```python
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admi_router)
```

#### Explanation

These lines attach the API routers to the main app so the defined endpoints become active.

- `auth_router` handles authentication routes such as register, login, refresh, and logout.
- `user_router` handles user-specific routes like profile access.
- `admin_router` handles admin-only endpoints.

#### Root Route

```python
@app.get("/")
def home():
    return {
        "message": "E-commerce backed API Running Successfully"
    }
```

#### Explanation

- `@app.get("/")` defines a GET endpoint for the root URL.
- `def home():` is the function that handles the request.
- The function returns a JSON response with a success message.

#### Health Route

```python
@app.get("/health")
def Health():
    return {
        "status": "healthy"
    }
```

#### Explanation

- `@app.get("/health")` defines a health check endpoint.
- `def Health():` handles the request and responds with the service status.
- This endpoint is useful for monitoring and deployment checks.

## API Endpoints Summary

### Authentication

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`

### User

- `GET /users/me`

### Admin

- `GET /admin/dashboard`

## Notes

- Use the Swagger UI at `/docs` for interactive API testing.
- Keep environment secrets in the `.env` file and never commit them to source control.
- Use Alembic migrations when changing database models.
