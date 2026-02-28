---
sidebar_position: 3
sidebar_label: "API Reference"
---

# 📡 API Reference

> **Base URL**: `http://localhost:8000/api`
>
> **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)

All v1 endpoints require a Bearer token via the `Authorization` header unless otherwise noted.

---

## 🔓 Auth — `/api/auth`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | ❌ | Register new user |
| `POST` | `/auth/login` | ❌ | Login (returns tokens + user) |
| `POST` | `/auth/refresh` | ❌ | Refresh access token |
| `POST` | `/auth/forgot-password` | ❌ | Request OTP for password reset |
| `POST` | `/auth/reset-password` | ❌ | Reset password with OTP |

### Register
```
POST /api/auth/register
Body: { "name": "John", "username": "john", "primary_email": "john@example.com", "password": "pass123" }
Response: { "access_token": "...", "refresh_token": "...", "token_type": "bearer" }
```

### Login
```
POST /api/auth/login (form-encoded)
Body: username=john&password=pass123
Response: { "access_token": "...", "refresh_token": "...", "token_type": "bearer", "user": {...} }
```

---

## 👤 Users — `/api/v1/users`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/` | Create a user |
| `GET` | `/users/` | List all users |
| `GET` | `/users/{user_id}` | Get user by ID |
| `PATCH` | `/users/{user_id}` | Update user |
| `DELETE` | `/users/{user_id}` | Delete user |

---

## 🏷️ Roles — `/api/v1/roles`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/roles/` | Create a role |
| `GET` | `/roles/` | List all roles |
| `GET` | `/roles/{role_id}` | Get role by ID |
| `PATCH` | `/roles/{role_id}` | Update role |
| `DELETE` | `/roles/{role_id}` | Delete role |

---

## 📂 Categories — `/api/v1/categories`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/categories/` | Create category (auto-assigns to current user) |
| `GET` | `/categories/` | List user's categories |
| `GET` | `/categories/{category_id}` | Get category by ID |
| `PATCH` | `/categories/{category_id}` | Update category |
| `DELETE` | `/categories/{category_id}` | Delete category |

---

## 💰 Transactions — `/api/v1/transactions`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/transactions/` | Create transaction |
| `GET` | `/transactions/` | List user's transactions |
| `GET` | `/transactions/{transaction_id}` | Get by ID |
| `PATCH` | `/transactions/{transaction_id}` | Update |
| `DELETE` | `/transactions/{transaction_id}` | Delete |

---

## 🔗 Connected Accounts — `/api/v1/connected-accounts`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/connected-accounts/` | Create connected account |
| `GET` | `/connected-accounts/` | List user's accounts |
| `GET` | `/connected-accounts/{account_id}` | Get by ID |
| `PATCH` | `/connected-accounts/{account_id}` | Update |
| `DELETE` | `/connected-accounts/{account_id}` | Delete |
| `GET` | `/connected-accounts/{account_id}/authorize` | Get OAuth authorization URL |
| `POST` | `/connected-accounts/{account_id}/fetch` | Trigger email fetch for account |

---

## ✉️ Emails — `/api/v1/emails`

| Method | Endpoint | Auth Scope | Description |
|--------|----------|------------|-------------|
| `POST` | `/emails/` | Own only | Create email |
| `GET` | `/emails/` | Admin: all, User: own | List emails |
| `GET` | `/emails/{email_id}` | Own only | Get by ID |
| `PATCH` | `/emails/{email_id}` | Own only | Update |
| `DELETE` | `/emails/{email_id}` | Own only | Delete |

---

## 🧬 Email Extractions — `/api/v1/email-extractions`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/email-extractions/` | Create extraction record |
| `GET` | `/email-extractions/` | List extractions |
| `GET` | `/email-extractions/{extraction_id}` | Get by ID |
| `PATCH` | `/email-extractions/{extraction_id}` | Update |
| `DELETE` | `/email-extractions/{extraction_id}` | Delete |

---

## ⚡ Jobs — `/api/v1/jobs`

| Method | Endpoint | Auth Scope | Description |
|--------|----------|------------|-------------|
| `POST` | `/jobs/trigger/fetch` | Auth | Trigger email fetch background job |
| `POST` | `/jobs/trigger/extract` | Auth | Trigger email extraction background job |
| `POST` | `/jobs/` | Auth | Create job record |
| `GET` | `/jobs/` | Admin: all, User: own | List jobs (filterable by status, type) |
| `GET` | `/jobs/{job_id}` | Auth | Get job by ID |
| `PATCH` | `/jobs/{job_id}` | Auth | Update job |
| `DELETE` | `/jobs/{job_id}` | Auth | Delete job |

### Trigger Email Fetch
```
POST /api/v1/jobs/trigger/fetch?provider=gmail&limit=20
Response: { "message": "Email fetch job enqueued" }
```

### Trigger Email Extraction
```
POST /api/v1/jobs/trigger/extract?batch_size=10
Response: { "message": "Email extraction job enqueued" }
```

---

## 🤖 LLM Transactions — `/api/v1/llm-transactions`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/llm-transactions/` | Create LLM usage record |
| `GET` | `/llm-transactions/` | List LLM transactions |
| `GET` | `/llm-transactions/{llm_tx_id}` | Get by ID |
| `PATCH` | `/llm-transactions/{llm_tx_id}` | Update |
| `DELETE` | `/llm-transactions/{llm_tx_id}` | Delete |

---

## 🔑 Google OAuth — `/api/v1/auth/google`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/auth/google/callback` | ❌ | OAuth2 callback (exchanges code for tokens) |

This is used internally by the OAuth flow initiated from `/connected-accounts/{id}/authorize`.

---

## Response Formats

**Success**: Returns the schema-defined JSON body with appropriate HTTP status code.

**Error**:
```json
{
  "detail": "Error message describing what went wrong"
}
```

Common status codes:
- `200` — OK
- `201` — Created
- `202` — Accepted (job enqueued)
- `204` — No Content (delete success)
- `400` — Bad Request
- `401` — Unauthorized
- `403` — Forbidden
- `404` — Not Found
