# E-Commerce Backend API

A FastAPI and PostgreSQL backend that currently provides authentication, user-profile management, refresh-token handling, and role-protected admin operations. It is a foundation for a larger e-commerce application; catalog, cart, order, and payment features are not implemented yet.

## Features

- Account registration with password validation
- JWT access and refresh tokens
- Refresh-token storage and logout invalidation
- Authenticated profile retrieval, updates, password changes, and account deactivation
- Role-based access for `customer`, `seller`, and `admin`
- Admin user listing, role updates, and account activation/deactivation
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
  services/       authentication and user-management logic
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

Send protected requests with:

```http
Authorization: Bearer <access_token>
```

## Development notes

- The initial migration creates the `users` and `refresh_tokens` tables.
- New model changes should be captured in a new Alembic migration before deployment.
- `Dockerfile` and `docker-compose.yml` are placeholders and do not yet provide a Docker workflow.
- There is no automated test suite checked in yet. Add API and service tests before relying on this in production.

For a more detailed walkthrough of the original authentication flow, see [NOTES.md](NOTES.md).
