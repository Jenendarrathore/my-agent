# Authentication Module Documentation

This document provides detailed information about the complete authentication system implemented in the application.

## 1. Database Architecture

### Models (`app/models/`)

#### [Role](file:///opt/gitco/ai/my-agent/app/models/role.py)
Standard Role-Based Access Control (RBAC) table.
- `id`: Integer (Primary Key, Serial)
- `name`: String (Unique, Indexed, e.g., "user", "admin")
- `created_at`: Timestamp (Timezone aware)

#### [User](file:///opt/gitco/ai/my-agent/app/models/user.py) (Updated)
- `id`: Integer (Primary Key, Serial)
- `name`: String (Optional, for display purposes)
- `username`: String (Unique, Indexed, Required)
- `primary_email`: String (Unique, Indexed, Required)
- `password_hash`: String (Stored using Bcrypt)
- `role_id`: Integer (Foreign Key to `roles.id`)
- `is_active`: Boolean (Defaults to `True`)
- `otp`: String (Numeric OTP, stored only when requested)
- `otp_expires_at`: Timestamp (OTP expiry time)
- `refresh_token`: String (Hashed version of the refresh token)
- `refresh_token_expiry`: Timestamp (Expiry for the refresh token)
- `created_at`: Timestamp (Timezone aware)

---

## 2. Security Infrastructure

### Library Versions
To ensure compatibility and security, the following versions are pinned in `requirements.txt`:
- `passlib==1.7.4`: For password hashing context.
- `bcrypt==3.2.0`: Modern hashing (pinned to fix library incompatibilities and the 72-byte limit).
- `python-jose[cryptography]`: For JWT generation and signing.

### JWT Configuration (`app/core/config.py`)
- `ALGORITHM`: HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 60 minutes
- `REFRESH_TOKEN_EXPIRE_DAYS`: 7 days

### Token Payloads
**Access Token:**
```json
{
  "sub": "user_id (string)",
  "role": "role_name",
  "type": "access",
  "exp": 1234567890
}
```

**Refresh Token:**
```json
{
  "sub": "user_id (string)",
  "type": "refresh",
  "exp": 1234567890
}
```

---

## 3. API Endpoints (`app/api/auth.py`)

### `POST /api/auth/register`
- **Input**: `username`, `primary_email`, `password`.
- **Action**: Assigns default "user" role, hashes password, saves to DB.
- **Output**: `access_token`, `refresh_token`, `token_type`.

### `POST /api/auth/login`
- **Input**: `username` and `password` (compatible with OAuth2 form data).
- **Identifier**: Supports both **email** and **username** as the login identifier.
- **Action**: Validates credentials, rotates/hashes refresh token in DB.
- **Output**: `access_token`, `refresh_token`, `token_type`, and `user` object.

### `POST /api/auth/refresh`
- **Input**: `refresh_token` (string).
- **Action**: Validates token signature, type, and database hash.
- **Output**: New `access_token`.

### `POST /api/auth/forgot-password`
- **Input**: `email`.
- **Action**: Generates 6-digit OTP, stores in **Database** (`users` table) with 5 min TTL, enqueues email worker.
- **Output**: Success message.

### `POST /api/auth/reset-password`
- **Input**: `email`, `otp`, `new_password`.
- **Action**: Verifies OTP from **Database**, hashes new password, invalidates OTP and sessions.
- **Output**: Success message.

---

## 4. Route Protection (`app/dependencies/auth.py`)

### `get_current_user` Dependency
This dependency protects routes and provides the authenticated user context.
- Decodes the JWT from the Authorization header (`Bearer <token>`).
- Validates token type (`access`).
- Checks if the user exists and is active.
- **Usage Example**:
```python
@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user
```

---

## 5. Swagger UI Integration

The API is fully integrated with Swagger's **"Authorize"** feature:
1. Navigate to `/docs`.
2. Click the **Authorize** button.
3. Enter your **username** (or email) and **password**.
4. Swagger will perform a `POST /api/auth/login` and store the token for all subsequent requests.

---

## 6. Project Structure Summary

| Component | File Path |
| :--- | :--- |
| Models | [role.py](file:///opt/gitco/ai/my-agent/app/models/role.py), [user.py](file:///opt/gitco/ai/my-agent/app/models/user.py) |
| Schemas | [auth.py](file:///opt/gitco/ai/my-agent/app/schemas/auth.py), [user.py](file:///opt/gitco/ai/my-agent/app/schemas/user.py) |
| Security Utils | [security.py](file:///opt/gitco/ai/my-agent/app/core/security.py) |
| CRUD Logic | [auth.py](file:///opt/gitco/ai/my-agent/app/crud/auth.py) |
| Dependencies | [auth.py](file:///opt/gitco/ai/my-agent/app/dependencies/auth.py) |
---

## 7. How to Test OTP (Developer Guide)

As a developer, you can test the forgot password flow without a real email server:

1.  **Trigger OTP**:
    - **Endpoint**: `POST /api/auth/forgot-password`
    - **Body**: `{"email": "your_email@example.com"}`
2.  **Retrieve OTP**:
    - Check the terminal logs where `uvicorn` or the `email_worker` is running.
    - Look for the `--- OTP EMAIL ---` block.
    - Copy the 6-digit code.
3.  **Reset Password**:
    - **Endpoint**: `POST /api/auth/reset-password`
    - **Body**: 
      ```json
      {
        "email": "your_email@example.com",
        "otp": "123456",
        "new_password": "securepassword123"
      }
      ```
4.  **Verify**: Log in with the new password via `POST /api/auth/login`.

| API Routes | [auth.py](file:///opt/gitco/ai/my-agent/app/api/auth.py) |
| Feature List | [features.md](file:///opt/gitco/ai/my-agent/features.md) |
| Developer Guide | [DEVELOPMENT.md](file:///opt/gitco/ai/my-agent/DEVELOPMENT.md) |
