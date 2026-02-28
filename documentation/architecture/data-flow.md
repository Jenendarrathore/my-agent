# 🔄 Data Flow & Request Lifecycle

## 1. Standard API Request Flow

Every authenticated API request follows this path:

```
Client (React)
  │
  │  HTTP Request + Bearer Token
  ▼
FastAPI Router
  │
  ├─ Depends(get_db)          → Creates AsyncSession from connection pool
  ├─ Depends(get_current_user) → Decodes JWT, loads User from DB with role
  │
  ▼
Router Handler Function
  │
  ├─ Validates request body (Pydantic schema)
  ├─ Calls Service layer method
  │
  ▼
Service Layer
  │
  ├─ Applies business logic
  ├─ Calls CRUD layer
  │
  ▼
CRUD Layer
  │
  ├─ Builds SQLAlchemy query
  ├─ Executes against PostgreSQL (async)
  │
  ▼
Response
  │
  ├─ Service returns Pydantic schema (Read model)
  ├─ Router returns HTTP response
  │
  ▼
Client receives JSON response
```

### Dependency Injection Details

| Dependency | Source | Purpose |
|-----------|--------|---------|
| `get_db` | `app.core.database` | Yields an `AsyncSession` scoped to the request |
| `get_current_user` | `app.dependencies.auth` | Decodes JWT → fetches full `User` with `role` |
| `oauth2_scheme` | FastAPI's `OAuth2PasswordBearer` | Extracts `Bearer` token from `Authorization` header |

---

## 2. Authentication Flow

### Registration
```
POST /api/auth/register
  │
  ├─ Validate UserRegister schema (name, username, email, password)
  ├─ Check email + username uniqueness
  ├─ get_default_role() → auto-creates "user" role if missing
  ├─ Hash password (bcrypt)
  ├─ Insert User to DB
  ├─ Generate access_token (JWT, 60min, includes user_id + role)
  ├─ Generate refresh_token (JWT, 7 days, includes user_id)
  ├─ Hash refresh_token, store in User.refresh_token column
  │
  └─ Return { access_token, refresh_token, token_type }
```

### Login
```
POST /api/auth/login (OAuth2PasswordRequestForm)
  │
  ├─ Lookup user by email OR username
  ├─ Verify password (bcrypt)
  ├─ Generate access_token with user_id + role_name
  ├─ Generate refresh_token
  ├─ Store hashed refresh_token in DB
  │
  └─ Return { access_token, refresh_token, token_type, user }
```

### Token Refresh
```
POST /api/auth/refresh
  │
  ├─ Decode refresh_token (JWT)
  ├─ Verify type == "refresh"
  ├─ Load user from DB
  ├─ Verify stored hashed refresh_token matches
  ├─ Check expiry
  ├─ Generate new access_token
  │
  └─ Return { access_token, refresh_token, token_type }
```

### Forgot Password + OTP
```
POST /api/auth/forgot-password
  │
  ├─ Lookup user by email
  ├─ Generate 6-digit OTP
  ├─ Store OTP + expiry (5 min) in User model columns
  ├─ Enqueue send_otp_email job via email_pool
  │
  └─ Return success message (always, to prevent enumeration)

POST /api/auth/reset-password
  │
  ├─ Lookup user by email
  ├─ Validate OTP matches + not expired
  ├─ Update password (bcrypt hash)
  ├─ Clear OTP, refresh_token, refresh_token_expiry
  │
  └─ Return success
```

---

## 3. Background Job Flow (Email Fetch Example)

```
Client
  │
  │  POST /api/v1/jobs/trigger/fetch?provider=gmail&limit=20
  ▼
Router (jobs.py)
  │
  ├─ Auth guard (get_current_user)
  ├─ TaskService.enqueue_email_fetch(user_id, provider, limit)
  │
  ▼
TaskService
  │
  ├─ Validates email_pool is initialized
  ├─ email_pool.enqueue_job("run_email_fetch", user_id, provider, limit)
  │   (Pushes to Redis DB 2)
  │
  ▼
ARQ Email Worker (separate process, listening on Redis DB 2)
  │
  ├─ Picks up "run_email_fetch"
  ├─ Opens a new AsyncSession (AsyncSessionLocal)
  ├─ Creates JobRunner(db)
  │
  ▼
JobRunner.run_job()
  │
  ├─ 1. Creates Job record (status: RUNNING)
  ├─ 2. Calls EmailFetchJob.before_run()
  ├─ 3. Calls EmailFetchJob.run()
  │       ├─ Gets ConnectedAccount from DB
  │       ├─ ProviderFactory.get_provider("gmail") → GmailProvider
  │       ├─ provider.connect(credentials)
  │       ├─ provider.fetch_messages(limit=20)
  │       ├─ Deduplicates against existing emails
  │       ├─ Stores new emails via EmailService
  │       └─ provider.disconnect()
  ├─ 4. Calls EmailFetchJob.after_run()
  ├─ 5. Updates Job record (status: SUCCESS, output_payload)
  │
  └─ If error → on_failure() → Job record (status: FAILED, error_payload)
```

---

## 4. Email Extraction Flow (LLM Processing)

```
POST /api/v1/jobs/trigger/extract?batch_size=10
  │
  ▼
TaskService.enqueue_email_extraction(batch_size=10)
  │  (Enqueues "run_email_extraction" to Redis DB 2)
  ▼
ARQ Email Worker
  │
  ▼
JobRunner → EmailExtractionJob.run()
  │
  ├─ SELECT emails WHERE extraction_status = 'PENDING' LIMIT batch_size
  │
  ├─ For each email:
  │    ├─ MockLLMService.extract_financial_data(email_text)
  │    ├─ Record LLMTransaction (tokens, cost, latency)
  │    ├─ Save EmailExtraction (result JSON, model, prompt_hash)
  │    ├─ If is_transaction:
  │    │    ├─ Find/create Category
  │    │    └─ Create Transaction (auto-extracted)
  │    └─ Update email.extraction_status → "COMPLETED" or "FAILED"
  │
  └─ Return { processed_count, transaction_count }
```

---

## 5. Google OAuth2 Flow (Connected Accounts)

```
1. User creates ConnectedAccount     → POST /api/v1/connected-accounts/
2. User initiates authorization      → GET /api/v1/connected-accounts/{id}/authorize
   │
   ├─ Build Google OAuth2 Flow
   ├─ Pass state = { account_id, user_id }
   └─ Return { authorization_url }  → Frontend redirects user to Google

3. Google redirects to callback      → GET /api/v1/auth/google/callback?code=...&state=...
   │
   ├─ Exchange authorization code for tokens
   ├─ Verify Google email matches account email
   ├─ Store access_token + refresh_token in ConnectedAccount
   └─ Redirect to frontend /dashboard?status=success

4. User triggers email fetch         → POST /api/v1/connected-accounts/{id}/fetch
   │
   └─ Uses stored tokens to fetch emails via GmailProvider
```

---

## 6. Multi-Tenant Access Control

The application implements role-based access control (RBAC):

| Role | Behavior |
|------|----------|
| **admin** | Can view ALL records (users, emails, jobs) across all users |
| **user** | Can only view/modify their OWN records |

**Implementation pattern** (used in routers):
```python
# Admin sees all, user sees only their own
user_id = None if current_user.role.name == "admin" else current_user.id
return await service.list_items(user_id=user_id)
```
