---
sidebar_position: 2
sidebar_label: "Authentication"
---

# 🔐 Authentication System

## Overview

The application uses **JWT-based authentication** with bcrypt password hashing and database-backed OTP for password reset.

---

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Security Utils | `app/core/security.py` | Password hash/verify, JWT create/decode |
| Auth Routes | `app/api/auth.py` | Register, login, refresh, forgot/reset password |
| Auth CRUD | `app/crud/auth.py` | User DB operations, token management |
| Auth Schemas | `app/schemas/auth.py` | Request/response models |
| Auth Dependency | `app/dependencies/auth.py` | `get_current_user` FastAPI dependency |
| OTP Utils | `app/core/otp.py` | OTP generation |

---

## Password Hashing

- **Library**: `passlib` with `bcrypt` scheme
- **Hash**: `get_password_hash(password)` — bcrypt hash
- **Verify**: `verify_password(plain, hashed)` — constant-time comparison

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

---

## JWT Tokens

### Access Token
- **Payload**: `{ sub: user_id, role: role_name, type: "access", exp: ... }`
- **Expiry**: 60 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Algorithm**: HS256
- **Signing key**: `SECRET_KEY` from env

### Refresh Token
- **Payload**: `{ sub: user_id, type: "refresh", exp: ... }`
- **Expiry**: 7 days (configurable via `REFRESH_TOKEN_EXPIRE_DAYS`)
- **Storage**: Hashed with bcrypt in `User.refresh_token` column
- **Verification**: Decoded from JWT, then hashed token compared against DB value

---

## Authentication Guard

The `get_current_user` dependency (`app/dependencies/auth.py`) protects all v1 routes:

```python
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)  # OAuth2PasswordBearer
) -> User:
```

**Steps**:
1. Extracts Bearer token from `Authorization` header
2. Decodes JWT using `decode_token()`
3. Validates `type == "access"` and `sub` exists
4. Loads full `User` object with `role` relationship (via `selectinload`)
5. Checks `user.is_active`
6. Returns `User` model instance (available in route handlers)

**Token URL**: `/api/auth/login` (configured in `OAuth2PasswordBearer`)

---

## Endpoints

### `POST /api/auth/register`
- **Input**: `UserRegister { name?, username, primary_email, password }`
- **Checks**: Email uniqueness, username uniqueness
- **Auto-assigns**: `"user"` role (created if missing)
- **Returns**: `{ access_token, refresh_token, token_type }`

### `POST /api/auth/login`
- **Input**: OAuth2 form (`username` can be email or username, `password`)
- **Returns**: `{ access_token, refresh_token, token_type, user }`
- **User object includes**: id, name, username, email, is_active, role `{ id, name }`

### `POST /api/auth/refresh`
- **Input**: `refresh_token` (query param)
- **Validates**: JWT decode, type check, DB hash verification, expiry check
- **Returns**: New `access_token`, same `refresh_token`

### `POST /api/auth/forgot-password`
- **Input**: `{ email }`
- **Action**: Generates 6-digit OTP, stores in User model, enqueues `send_otp_email` job
- **Response**: Always returns success message (prevents email enumeration)

### `POST /api/auth/reset-password`
- **Input**: `{ email, otp, new_password }`
- **Validates**: OTP matches and not expired (5-minute window)
- **Action**: Updates password, clears OTP, invalidates refresh token

---

## OTP System

- **Storage**: Database-backed (in `User.otp` and `User.otp_expires_at` columns)
- **Expiry**: 5 minutes (`OTP_EXPIRY = 300`)
- **Delivery**: Via ARQ email worker (`send_otp_email` task)
- **Generation**: 6 random digits via `random.choices(string.digits, k=6)`

---

## Role-Based Access Control (RBAC)

| Role | Capabilities |
|------|-------------|
| `admin` | View ALL records across all users |
| `user` | View/modify only OWN records |

**Pattern used in routes**:
```python
user_id = None if current_user.role.name == "admin" else current_user.id
```

Roles are stored in the `roles` table and linked to users via `role_id` FK.

---

## Frontend Auth Flow

1. **Login**: POST to `/api/auth/login` → stores `access_token` and `user` in `localStorage`
2. **Protected Routes**: `ProtectedRoute` component checks `localStorage.getItem("access_token")`
3. **API Calls**: Bearer token included in `Authorization` header via axios
4. **Logout**: Removes `access_token` and `user` from `localStorage`, redirects to `/login`
