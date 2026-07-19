# Project Notes

This document provides a professional and easy-to-understand explanation of the main backend file and the application flow.

## 1. File Overview

### `app/main.py`

This is the entry point of the FastAPI application. It is responsible for:

- creating the application instance
- storing the project metadata such as title and version
- loading all API route modules
- exposing the base and health endpoints

## 2. Application Initialization

### Syntax

```python
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)
```

### Explanation

The `FastAPI()` function creates the main application object.

- `title=settings.PROJECT_NAME` sets the API name using the environment configuration.
- `version=settings.API_VERSION` sets the application version.

This is the starting point for the entire backend service.

## 3. Router Registration

### Syntax

```python
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admi_router)
```

### Explanation

These statements register different route groups into the FastAPI application.

- `auth_router` handles authentication operations such as register, login, token refresh, and logout.
- `user_router` handles user-specific operations like viewing the current user profile.
- `admi_router` handles admin-only routes such as the admin dashboard.

By registering these routers, all endpoint functions become available through the API.

## 4. Home Route

### Syntax

```python
@app.get("/")
def home():
    return {
        "message": "E-commerce backed API Running Successfully"
    }
```

### Explanation

- `@app.get("/")` defines a GET request for the root path.
- `def home()` is the function that runs when the route is called.
- The function returns a JSON response showing that the API is running successfully.

This route is often used as a quick sanity check during development.

## 5. Health Check Route

### Syntax

```python
@app.get("/health")
def Health():
    return {
        "status": "healthy"
    }
```

### Explanation

- `@app.get("/health")` creates a health check endpoint.
- The function returns a simple status message.
- This endpoint is useful for monitoring systems, deployment checks, and uptime verification.

## 6. Request Flow Summary

The request flow in this file is straightforward:

1. The client sends a request to the FastAPI application.
2. The app checks the route configuration.
3. The corresponding router handles the request.
4. The logic inside the endpoint returns a response in JSON format.

## 7. Practical Use

This file is important because it ties all parts of the backend together.

Without this file:

- the application would not start
- routes would not be attached
- the server would not respond to API requests

## 8. Best Practices

- Keep the startup file minimal and clean.
- Register routes only through dedicated router modules.
- Use environment-based settings rather than hardcoded values.
- Keep the root and health endpoints simple and reliable.

## 9. Authentication Module Notes

### File: `app/api/auth.py`

This file defines the authentication-related API routes. It is responsible for user registration, login, token refresh, and logout functionality.

### Route Structure

```python
router = APIRouter(
    prefix="/auth",
    tags=["Authetication"],
)
```

### Explanation

- `APIRouter()` creates a modular router for the authentication endpoints.
- `prefix="/auth"` ensures all routes in this file are accessed under the `/auth` path.
- `tags=["Authetication"]` groups these endpoints in the generated OpenAPI documentation.

### Register Endpoint

```python
@router.post(
    "/register",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user: UserCreate, db: Session = Depends(get_db)):
```

### Explanation

- `@router.post("/register")` creates a POST endpoint for user registration.
- `response_model=ApiResponse` ensures the response follows a standard API structure.
- `status_code=201` indicates that a new user resource has been created.
- `user: UserCreate` receives the incoming registration payload.
- `db: Session = Depends(get_db)` injects the database session for database interaction.

### Login Endpoint

```python
@router.post("/login", response_model=ApiResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
```

### Explanation

This endpoint authenticates a user by validating the provided login payload and returning a response object containing authentication details.

### Refresh Token Endpoint

```python
@router.post("/refresh", response_model=ApiResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
```

### Explanation

This route accepts a refresh token and returns a new access token when the token is valid.

### Logout Endpoint

```python
@router.post("/logout", response_model=ApiResponse)
def logout(request: RefreshTokenRequest, db: Session = Depends(get_db)):
```

### Explanation

This endpoint invalidates the refresh token and ends the user session securely.

## 10. User Module Notes

### File: `app/api/user.py`

This file contains routes associated with the authenticated user profile.

### Router Setup

```python
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
```

### Explanation

- The router is prefixed with `/users`.
- All routes in this module are grouped under the `Users` tag.

### Profile Endpoint

```python
@router.get("/me", response_model=ApiResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
```

### Explanation

- `@router.get("/me")` defines a GET route for viewing the current authenticated user's profile.
- `current_user: User = Depends(get_current_user)` uses the dependency to fetch the logged-in user from the token.
- The response is returned in a standardized API response structure.

## 11. Admin Module Notes

### File: `app/api/admin.py`

This file defines routes intended for administrative users only.

### Router Setup

```python
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)
```

### Explanation

- The router prefix is `/admin`, keeping admin routes separated from user routes.
- The endpoint group is labeled as `Admin` in the OpenAPI docs.

### Admin Dashboard Route

```python
@router.get("/dashboard", response_model=ApiResponse)
def admin_dashboard(current_admin: User = Depends(get_current_admin)):
```

### Explanation

- `@router.get("/dashboard")` creates an admin-only dashboard endpoint.
- `Depends(get_current_admin)` ensures only an authenticated admin can access it.
- The returned data is formatted using the shared `ApiResponse` schema.

## 12. Summary of API Responsibilities

- `auth.py` handles user identity and token operations.
- `user.py` handles the authenticated user's self-profile data.
- `admin.py` restricts access to administrative functionality.

This separation improves maintainability, readability, and security by keeping each route responsibility in its own module.
