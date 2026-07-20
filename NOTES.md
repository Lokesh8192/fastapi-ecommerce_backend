# Project Notes

This document describes the current backend structure and the main application flows.

## Application entry point

### `app/main.py`

`app/main.py` creates the FastAPI application, loads configuration, and registers every router:

```python
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(category_router)
app.include_router(product_router)
```

It also exposes:

- `GET /` — basic API status message
- `GET /health` — health-check response

## Modules and responsibilities

| Module | Responsibility |
| --- | --- |
| `app/api/auth.py` | Registration, login, refresh tokens, and logout |
| `app/api/user.py` | Current-user profile operations |
| `app/api/admin.py` | Admin dashboard and user administration |
| `app/api/category.py` | Category creation, bulk creation, reads, updates, and activation state |
| `app/api/product.py` | Product creation, reads, updates, and activation state |
| `app/services/` | Business rules and validation |
| `app/repositories/` | Database queries and transactions |
| `app/models/` | SQLAlchemy table definitions |
| `app/schemas/` | Pydantic request and response validation |

## Authentication and authorization

The API uses JWT access tokens. Protected routes receive the authenticated user through FastAPI dependencies.

- `get_current_user` validates the bearer token and loads the associated user.
- `get_current_active_user` also requires an active account.
- `get_current_admin` requires an active account with the `admin` role.

Category and product writes require an admin token. Their `created_by` fields are set automatically from the authenticated admin ID; clients do not send this value in request bodies.

## Swagger workflow

1. Open `http://127.0.0.1:8000/docs`.
2. Call `POST /auth/login` with an admin account.
3. Copy the returned access token.
4. Select **Authorize** in Swagger and enter `Bearer <access_token>`.
5. Call protected routes.

Use `GET /users/me` to view the currently authenticated user and ID.

## Category management

### Single category creation

`POST /categories` creates one category. The request contains a name and description; the API assigns the logged-in admin to `created_by`.

### Bulk category creation

`POST /categories/bulk` creates from 1 to 100 categories in one request.

```json
{
  "categories": [
    {
      "name": "Furniture",
      "description": "Tables, chairs, sofas, and home furnishings."
    },
    {
      "name": "Mobile Phones",
      "description": "Smartphones, feature phones, and mobile accessories."
    }
  ]
}
```

The bulk operation validates duplicate names both within the request and against the database. It uses one transaction: if any category cannot be saved, the whole batch is rolled back.

### Category access rules

- `GET /categories` and `GET /categories/{category_id}` require any authenticated user.
- Creating, updating, activating, and deactivating categories require an admin.
- Only active categories are returned by the category list endpoint.

## Product management

A product belongs to a category through `category_id` and is owned by the authenticated admin through `created_by`.

```json
{
  "name": "Wireless Bluetooth Earbuds",
  "description": "Compact true wireless earbuds with charging case.",
  "price": 2499.00,
  "stock": 40,
  "image_url": "https://example.com/images/earbuds.jpg",
  "category_id": 1
}
```

When creating a product, the service verifies that the requested category exists and is active. A product with the same name cannot be added twice to the same category.

### Product access rules

- `GET /products` and `GET /products/{product_id}` require any authenticated user.
- Creating, updating, activating, and deactivating products require an admin.

## Request flow

1. The client sends an HTTP request.
2. FastAPI matches the route in an API router.
3. Dependencies validate the token and permissions when needed.
4. The route calls a service method.
5. The service applies business rules and calls a repository.
6. The repository reads or writes PostgreSQL through SQLAlchemy.
7. The route returns the standard `ApiResponse` JSON shape.

## Database and migrations

SQLAlchemy models define the users, refresh tokens, categories, and products tables. Alembic migrations must be applied before running the application:

```powershell
alembic upgrade head
```

Create a new migration whenever a model schema changes. Test migrations on a non-production database before deployment.

## Development guidance

- Keep route handlers focused on HTTP input and output.
- Put business rules in services and queries in repositories.
- Validate database foreign keys and active-state rules before writes.
- Use environment variables for database URLs and secrets.
- Add API and service tests before deploying to production.
