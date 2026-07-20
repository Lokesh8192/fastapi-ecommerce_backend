# E-Commerce Backend API

A FastAPI and PostgreSQL backend for authentication, user management, category management, and product catalog management. Cart, order, and payment features are not implemented yet.

## Features

- Account registration with password validation
- JWT access and refresh tokens
- Refresh-token storage and logout invalidation
- Authenticated profile retrieval, updates, password changes, and account deactivation
- Role-based access for `customer`, `seller`, and `admin`
- Admin user listing, role updates, and account activation/deactivation
- Admin-managed categories, including bulk category creation
- Admin-managed products linked to categories
- Automatic ownership (`created_by`) from the authenticated admin account
- SQLAlchemy models and Alembic database migrations

## Stack

- Python 3
- FastAPI and Uvicorn
- SQLAlchemy with PostgreSQL
- Alembic
- Pydantic Settings
- `python-jose` and Passlib for JWTs and password hashing

## Project layout

```text
app/
  api/            HTTP route handlers
  core/           configuration, security, roles, and dependencies
  db/             engine, session, and SQLAlchemy base
  models/         database models
  repositories/   database access helpers
  schemas/        request and response models
  services/       authentication, category, and product business logic
alembic/          database migration configuration and revisions
```

## Setup

1. Create and activate a virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

3. Create `.env` in the project root. Use a strong, private `SECRET_KEY`; do not commit this file.

   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/ecommerce_db
   TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/ecommerce_test_db
   SECRET_KEY=replace-with-a-long-random-secret
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   PROJECT_NAME=E-Commerce Backend API
   API_VERSION=v1
   DEBUG=False
   ```

4. Create the PostgreSQL database and apply migrations.

   ```powershell
   alembic upgrade head
   ```

5. Start the development server.

   ```powershell
   uvicorn app.main:app --reload
   ```

Open [Swagger UI](http://127.0.0.1:8000/docs) to explore the API. The health check is available at `GET /health`.

## API routes

| Area | Method | Route | Authentication |
| --- | --- | --- | --- |
| System | `GET` | `/` | None |
| System | `GET` | `/health` | None |
| Auth | `POST` | `/auth/register` | None |
| Auth | `POST` | `/auth/login` | None |
| Auth | `POST` | `/auth/refresh` | None |
| Auth | `POST` | `/auth/logout` | None |
| User | `GET` | `/users/me` | Access token |
| User | `PUT` | `/users/me` | Access token |
| User | `PUT` | `/users/change-password` | Access token |
| User | `DELETE` | `/users/me` | Access token |
| Admin | `GET` | `/admin/dashboard` | Admin token |
| Admin | `GET` | `/admin/users` | Admin token |
| Admin | `GET` | `/admin/users/{user_id}` | Admin token |
| Admin | `PUT` | `/admin/users/{user_id}/role` | Admin token |
| Admin | `PATCH` | `/admin/users/{user_id}/activate` | Admin token |
| Admin | `PATCH` | `/admin/users/{user_id}/deactivate` | Admin token |
| Categories | `POST` | `/categories` | Admin token |
| Categories | `POST` | `/categories/bulk` | Admin token |
| Categories | `GET` | `/categories` | Access token |
| Categories | `GET` | `/categories/{category_id}` | Access token |
| Categories | `PUT` | `/categories/{category_id}` | Admin token |
| Categories | `PATCH` | `/categories/{category_id}/activate` | Admin token |
| Categories | `PATCH` | `/categories/{category_id}/deactivate` | Admin token |
| Products | `POST` | `/products` | Admin token |
| Products | `GET` | `/products` | Access token |
| Products | `GET` | `/products/{product_id}` | Access token |
| Products | `PUT` | `/products/{product_id}` | Admin token |
| Products | `PATCH` | `/products/{product_id}/activate` | Admin token |
| Products | `PATCH` | `/products/{product_id}/deactivate` | Admin token |

Send protected requests with:

```http
Authorization: Bearer <access_token>
```

## Swagger workflow

1. Call `POST /auth/login` with an admin account.
2. Copy the `access_token` from the response.
3. In Swagger UI, select **Authorize** and enter `Bearer <access_token>`.
4. Call protected endpoints. Category and product creation use the logged-in admin ID automatically; do not include `created_by` in the request body.

Use `GET /users/me` to view the current authenticated user's ID and profile.

## Bulk category creation

`POST /categories/bulk` accepts 1 to 100 categories and saves them in a single transaction. Names must be unique within the request and must not already exist in the database.

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

## Product creation

Products must reference an existing active category through `category_id`. The `created_by` value is assigned from the current authenticated admin.

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

## Development notes

- Migrations create the users, refresh-token, category, and product tables.
- New model changes should be captured in a new Alembic migration before deployment.
- `Dockerfile` and `docker-compose.yml` are placeholders and do not yet provide a Docker workflow.
- There is no automated test suite checked in yet. Add API and service tests before relying on this in production.

For a more detailed walkthrough of the original authentication flow, see [NOTES.md](NOTES.md).
