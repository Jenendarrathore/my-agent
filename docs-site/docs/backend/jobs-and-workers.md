---
sidebar_position: 6
sidebar_label: "Jobs & Workers"
---

# ⚡ Jobs & Workers System

## Overview

The application uses **ARQ** (Async Redis Queue) for background job processing with a **multi-queue architecture** using logical Redis database isolation.

---

## Architecture

```
┌─────────────────────┐     ┌─────────────────────────────────┐
│   FastAPI API        │     │          Redis                  │
│                      │     │                                 │
│  TaskService         │────▶│  DB 1 → Base Queue              │
│   .enqueue_email_*() │────▶│  DB 2 → Email Queue             │
└─────────────────────┘     └──────────┬──────────────────────┘
                                       │
                        ┌──────────────▼──────────────────────┐
                        │         ARQ Workers                  │
                        │                                      │
                        │  Base Worker (DB 1)                   │
                        │   └─ sample_task                     │
                        │                                      │
                        │  Email Worker (DB 2)                  │
                        │   ├─ send_email                      │
                        │   ├─ send_otp_email                  │
                        │   ├─ run_email_fetch    ─┐           │
                        │   └─ run_email_extraction│           │
                        │                          ▼           │
                        │            ┌─────────────────┐       │
                        │            │  JobRunner       │       │
                        │            │  ├─ BaseJob      │       │
                        │            │  ├─ EmailFetchJob│       │
                        │            │  └─ EmailExtract │       │
                        │            └─────────────────┘       │
                        └──────────────────────────────────────┘
```

---

## Worker Configuration

### Base Worker (`app/core/worker/base_settings.py`)
```python
class WorkerSettings:
    functions = [sample_task]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    redis_settings.database = 1  # Redis DB 1
    on_startup = startup
    on_shutdown = shutdown
```

### Email Worker (`app/core/worker/email_settings.py`)
```python
class WorkerSettings:
    functions = [send_email, send_otp_email, run_email_fetch, run_email_extraction]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    redis_settings.database = 2  # Redis DB 2
    on_startup = startup
    on_shutdown = shutdown
```

---

## Running Workers

```bash
# Base Worker
./venv/bin/arq app.core.worker.base_settings.WorkerSettings
# or: python run_base_worker.py

# Email Worker
./venv/bin/arq app.core.worker.email_settings.WorkerSettings
# or: python run_email_worker.py
```

---

## ARQ Pool Initialization

During app startup (`app/core/setup.py`), the lifespan creates two ARQ connection pools:

```python
async def create_redis_queue_pools() -> None:
    queue.base_pool = await create_pool(BaseWorkerSettings.redis_settings)   # DB 1
    queue.email_pool = await create_pool(EmailWorkerSettings.redis_settings)  # DB 2
```

These pools are used by `TaskService` to enqueue jobs from the API.

---

## Task Functions (`app/workers/jobs.py`)

These are the **ARQ task functions** registered with workers:

| Function | Worker | Purpose |
|----------|--------|---------|
| `sample_task(ctx)` | Base | Demo task |
| `send_email(ctx, user_id)` | Email | Send generic email |
| `send_otp_email(ctx, email, otp)` | Email | Send OTP for password reset |
| `run_email_fetch(ctx, user_id, provider, limit, account_id)` | Email | Fetch emails via provider |
| `run_email_extraction(ctx, batch_size)` | Email | Extract data via LLM |

**Key pattern**: `run_email_fetch` and `run_email_extraction` open their own `AsyncSession` and use `JobRunner`:
```python
async def run_email_fetch(ctx, user_id, provider="gmail", limit=20, account_id=None):
    async with AsyncSessionLocal() as db:
        runner = JobRunner(db)
        payload = {"user_id": user_id, "provider": provider, "limit": limit, "account_id": account_id}
        await runner.run_job(EmailFetchJob, "EMAIL_FETCH", payload, triggered_by="system", user_id=user_id)
```

---

## Job Lifecycle (BaseJob + JobRunner)

### BaseJob (`app/jobs/base.py`)
Abstract base class for all jobs. Subclasses must implement `run()`.

```python
class BaseJob(ABC):
    def __init__(self, db: AsyncSession, input_payload: dict):
        self.db = db
        self.input_payload = input_payload or {}
        self.job_record: Optional[Job] = None

    @abstractmethod
    async def run(self) -> Any: ...          # Main logic
    async def before_run(self, job): ...     # Hook before execution
    async def after_run(self, result): ...   # Hook after success
    async def on_failure(self, error): ...   # Hook on failure
```

### JobRunner (`app/jobs/base.py`)
Orchestrates the full job lifecycle:

```
1. Create Job record (status: RUNNING)
2. Call job.before_run()
3. Update started_at timestamp
4. Call job.run()
5. Call job.after_run()
6. Update Job record (status: SUCCESS, output_payload)
   — OR on exception —
6. Call job.on_failure()
7. Update Job record (status: FAILED, error_payload with traceback)
```

### Job Status Lifecycle
```
QUEUED → RUNNING → SUCCESS
                 → FAILED
                 → CANCELLED
```

---

## Existing Jobs

### `EmailFetchJob` (`app/jobs/email_fetch.py`)
1. Gets `ConnectedAccount` credentials from DB
2. Creates provider via `ProviderFactory`
3. Connects with OAuth tokens
4. Fetches messages (paginated)
5. Deduplicates against existing emails
6. Stores new emails via `EmailService`
7. Returns `{ fetched_count, saved_count, user_id }`

### `EmailExtractionJob` (`app/jobs/email_extraction.py`)
1. Queries PENDING emails (batched)
2. For each email:
   - Calls `MockLLMService.extract_financial_data()`
   - Records `LLMTransaction` (token usage, cost)
   - Saves `EmailExtraction` result
   - If is_transaction: creates `Transaction` + finds/creates `Category`
3. Updates email `extraction_status`
4. Returns `{ processed_count, transaction_count }`

---

## Enqueuing Jobs from API

Use `TaskService` (static methods):

```python
# From a route handler:
await TaskService.enqueue_email_fetch(user_id=1, provider="gmail", limit=20)
await TaskService.enqueue_email_extraction(batch_size=10)
```

Or trigger via API endpoints:
```bash
POST /api/v1/jobs/trigger/fetch?provider=gmail&limit=20
POST /api/v1/jobs/trigger/extract?batch_size=10
```
