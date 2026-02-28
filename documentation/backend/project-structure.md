# 📁 Project Structure

## Root Directory

```
my-agent/
├── app/                          # Backend application
│   ├── __init__.py
│   ├── main.py                   # FastAPI entry point
│   ├── api/                      # API route definitions
│   ├── core/                     # Infrastructure & config
│   ├── crud/                     # Data access layer
│   ├── dependencies/             # FastAPI dependency injectors
│   ├── email/                    # Email provider abstraction
│   ├── jobs/                     # Background job definitions
│   ├── models/                   # SQLAlchemy models
│   ├── schemas/                  # Pydantic schemas
│   ├── scripts/                  # Utility & test scripts
│   ├── services/                 # Business logic layer
│   └── workers/                  # ARQ worker task functions
├── alembic/                      # Database migration files
│   ├── env.py                    # Migration environment config
│   ├── script.py.mako            # Migration template
│   └── versions/                 # Migration version files
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── components/           # Shared components (MainLayout)
│   │   ├── pages/                # Page components
│   │   ├── App.tsx               # Root with routing
│   │   └── main.tsx              # React DOM entry
│   ├── package.json
│   └── vite.config.ts
├── .env                          # Environment variables (not in git)
├── .env.example                  # Example env file
├── alembic.ini                   # Alembic configuration
├── docker-compose.yml            # Docker multi-service config
├── Dockerfile                    # Python container image
├── migrate.sh                    # Quick migration script
├── requirements.txt              # Python dependencies
├── run_base_worker.py            # Base worker runner
└── run_email_worker.py           # Email worker runner
```

---

## Backend — Layer by Layer

### `app/core/` — Infrastructure & Configuration

| File | Purpose |
|------|---------|
| `config.py` | `Settings` class (Pydantic) — loads all env vars from `.env` |
| `database.py` | Async SQLAlchemy engine, `AsyncSessionLocal`, `Base`, `get_db()` dependency |
| `security.py` | Password hashing (bcrypt), JWT creation & decoding |
| `redis.py` | Async Redis client lifecycle (`init_redis`, `close_redis`, `get_redis`) |
| `queue.py` | Global ARQ pool placeholders (`base_pool`, `email_pool`) |
| `otp.py` | OTP generator (6-digit random numeric) |
| `setup.py` | Application factory (`create_application`), lifespan management, CORS |
| `worker/base_settings.py` | Base worker config (Redis DB 1, registers `sample_task`) |
| `worker/email_settings.py` | Email worker config (Redis DB 2, registers email tasks) |

### `app/models/` — SQLAlchemy Models

| File | Model | Table |
|------|-------|-------|
| `user.py` | `User` | `users` |
| `role.py` | `Role` | `roles` |
| `category.py` | `Category` | `categories` |
| `transaction.py` | `Transaction` | `transactions` |
| `connected_account.py` | `ConnectedAccount` | `connected_accounts` |
| `email.py` | `Email` | `emails` |
| `email_extraction.py` | `EmailExtraction` | `email_extractions` |
| `job.py` | `Job` | `jobs` |
| `llm_transaction.py` | `LLMTransaction` | `llm_transactions` |

### `app/schemas/` — Pydantic Schemas

Each model has a corresponding schema module with:
- **`Base`** — Shared fields
- **`Create`** — Input for creation
- **`Update`** — Partial update fields (optional)
- **`Read`** — Full output with `model_config = ConfigDict(from_attributes=True)`

Plus `auth.py` with `UserRegister`, `UserLogin`, `Token`, `LoginResponse`, etc.

### `app/crud/` — Data Access Functions

Each module provides async functions:
- `create_<entity>(db, obj_in)` — INSERT and return
- `get_<entity>(db, id)` — SELECT by PK
- `get_<entities>(db, skip, limit, filters)` — SELECT with pagination/filters
- `update_<entity>(db, db_obj, obj_in)` — Partial UPDATE
- `delete_<entity>(db, id)` — DELETE

Special: `auth.py` handles user lookups, password verification, token management.

### `app/services/` — Business Logic

| Service | Purpose |
|---------|---------|
| `UserService` | User CRUD operations |
| `CategoryService` | Category management with name lookups |
| `TransactionService` | Transaction CRUD |
| `ConnectedAccountService` | OAuth account management |
| `EmailService` | Email storage + provider-ID deduplication |
| `EmailExtractionService` | LLM extraction result storage |
| `JobService` | Job record management + `create_job_raw()` |
| `LLMTransactionService` | LLM cost tracking |
| `RoleService` | Role management |
| `TaskService` | **Static** — enqueues jobs to ARQ pools |
| `MockLLMService` | Simulated LLM for email extraction |

### `app/api/` — Route Definitions

| File | Prefix | Purpose |
|------|--------|---------|
| `auth.py` | `/api/auth` | Register, login, refresh, forgot/reset password |
| `v1/users.py` | `/api/v1/users` | User CRUD |
| `v1/roles.py` | `/api/v1/roles` | Role CRUD |
| `v1/categories.py` | `/api/v1/categories` | Category CRUD |
| `v1/transactions.py` | `/api/v1/transactions` | Transaction CRUD |
| `v1/connected_accounts.py` | `/api/v1/connected-accounts` | Account CRUD + authorize + fetch |
| `v1/emails.py` | `/api/v1/emails` | Email CRUD |
| `v1/email_extractions.py` | `/api/v1/email-extractions` | Extraction CRUD |
| `v1/jobs.py` | `/api/v1/jobs` | Job CRUD + trigger endpoints |
| `v1/llm_transactions.py` | `/api/v1/llm-transactions` | LLM usage CRUD |
| `v1/google_auth.py` | `/api/v1/auth/google` | Google OAuth2 callback |

### `app/jobs/` — Background Job Definitions

| File | Class | Purpose |
|------|-------|---------|
| `base.py` | `BaseJob` | Abstract job class with lifecycle hooks |
| `base.py` | `JobRunner` | Orchestrator — creates records, runs lifecycle |
| `email_fetch.py` | `EmailFetchJob` | Fetches emails via provider abstraction |
| `email_extraction.py` | `EmailExtractionJob` | Processes emails with LLM |

### `app/email/` — Email Provider Abstraction

| File | Purpose |
|------|---------|
| `dto.py` | `EmailMessage` — normalized DTO |
| `exceptions.py` | `EmailProviderError`, `EmailAuthError`, `EmailFetchError`, `EmailRateLimitError` |
| `providers/base.py` | `EmailProvider` abstract class |
| `providers/gmail.py` | `GmailProvider` — Gmail API implementation |
| `providers/factory.py` | `ProviderFactory` — registry pattern |

### `app/workers/` — ARQ Task Functions

| File | Functions |
|------|-----------|
| `jobs.py` | `run_email_fetch`, `run_email_extraction`, `sample_task`, `send_email`, `send_otp_email` |

### `app/scripts/` — Utility Scripts

| File | Purpose |
|------|---------|
| `cleanup_db.py` | Database cleanup utility |
| `setup_user_gmail.py` | Set up Gmail for a user |
| `test_api_crud.py` | API CRUD integration tests |
| `test_email_abstraction.py` | Email provider tests |
| `test_gmail_structure.py` | Gmail API structure tests |
| `test_job_system.py` | Job system tests |
| `test_roles_crud.py` | Role CRUD tests |
