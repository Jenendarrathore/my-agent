# 🧩 Service Layer

## Overview

Services contain **business logic** and act as an intermediary between API routers and CRUD functions. All services follow a consistent pattern:

```python
class XxxService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # Methods call CRUD and return Pydantic schemas
```

---

## All Services

### `UserService` — `app/services/user_service.py`
Standard CRUD operations for users.
- `create_user(user_in)` → `UserRead`
- `get_user(id)` → `Optional[UserRead]`
- `list_users(skip, limit)` → `List[UserRead]`
- `update_user(id, user_in)` → `Optional[UserRead]`
- `delete_user(id)` → `bool`

### `RoleService` — `app/services/role_service.py`
Role management for RBAC.
- Standard CRUD operations for roles.

### `CategoryService` — `app/services/category_service.py`
Category management with name-based lookups.
- Standard CRUD + `get_category_by_name(user_id, name)` for finding existing categories.

### `TransactionService` — `app/services/transaction_service.py`
Financial transaction management.
- `create_transaction(tx_in, user_id)` — creates with user ownership.
- Standard list/get/update/delete.

### `ConnectedAccountService` — `app/services/connected_account_service.py`
OAuth account management.
- `create_account(account_in, user_id)` — creates linked to user.
- `list_user_accounts(user_id)` — schema-based return.
- `list_user_accounts_db(user_id)` — raw model return (used by workers).
- `get_account_db(account_id)` — raw model return (used by workers).
- Standard update/delete.

### `EmailService` — `app/services/email_service.py`
Email record management with deduplication.
- `get_email_by_provider_id(user_id, provider, provider_message_id)` — dedup lookup.
- `list_user_emails(user_id, skip, limit)` — supports `user_id=None` for admin.
- Standard CRUD.

### `EmailExtractionService` — `app/services/email_extraction_service.py`
LLM extraction result storage.
- `create_extraction(extraction_in)` — stores extraction results.
- Standard CRUD.

### `JobService` — `app/services/job_service.py`
Job record management with advanced filtering.
- `create_job_raw(**kwargs)` — internal helper returning raw model (used by `JobRunner`).
- `list_jobs(skip, limit, status, job_type, user_id)` — filterable listing.
- Standard CRUD.

### `LLMTransactionService` — `app/services/llm_transaction_service.py`
LLM API usage and cost tracking.
- `create_transaction(tx_in)` — records token usage, cost, latency.
- Standard CRUD.

### `TaskService` — `app/services/task_service.py`
**Static service** — enqueues background jobs to ARQ pools.

```python
class TaskService:
    @staticmethod
    async def enqueue_email_fetch(user_id, provider="gmail", limit=20, account_id=None):
        await queue.email_pool.enqueue_job("run_email_fetch", ...)
    
    @staticmethod
    async def enqueue_email_extraction(batch_size=10):
        await queue.email_pool.enqueue_job("run_email_extraction", ...)
```

**Important**: Validates that the pool is initialized before enqueueing. Raises `RuntimeError` if pools aren't ready.

### `MockLLMService` — `app/services/llm.py`
Simulated LLM for email financial data extraction.

```python
class MockLLMService:
    async def extract_financial_data(self, email_text: str) -> LLMResponse:
        # Returns simulated extraction with:
        # - amount, currency, merchant, category
        # - Token counts, latency
        # - Keyword-based merchant detection (uber → Transport, amazon → Shopping)
```

Returns `LLMResponse` dataclass with `content`, `model_name`, `prompt_hash`, `input_tokens`, `output_tokens`, `latency_ms`.

---

## Service Conventions

| Convention | Description |
|-----------|-------------|
| **Constructor** | Takes `db: AsyncSession` |
| **Returns** | Pydantic schema (not raw model), except `*_raw()` and `*_db()` methods |
| **No HTTP logic** | Services don't know about requests, status codes, or exceptions |
| **Stateless** | Created per request, no shared state |
| **Transactions** | CRUD handles commit; services may call `db.commit()` in complex flows |
