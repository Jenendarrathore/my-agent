# Project Architecture & Reference Guide 🏗️

This document explains the technical reasoning, design patterns, and infrastructure orchestration behind the FastAPI Boilerplate.

## 1. Clean Architecture Design
The project is organized to ensure a strict separation between infrastructure (how we store data) and domain logic (what we do with data).

| Component | Responsibility | Technical Tool |
| :--- | :--- | :--- |
| **`app/main.py`** | Application entry point and router inclusion. | Uvicorn / FastAPI |
| **`app/core/setup.py`** | Centralized factory for app creation and specialized infrastructure (lifespan). | FastAPI Lifespan |
| **`app/core/queue.py`** | A pure state container for ARQ pool placeholders. | ARQ / Redis |
| **`app/core/worker/`** | Specialized configurations for background worker processes. | ARQ Settings |
| **`app/models/`** | Async SQLAlchemy table definitions. | SQLAlchemy 2.0 |
| **`app/schemas/`** | Data validation and API serialization. | Pydantic V2 |
| **`app/services/`** | Reusable business logic (domain layer). | Python Async |
| **`app/workers/`** | Background job logic (functions). | ARQ Jobs |

---

## 2. Centralized Application Factory (`setup.py`)
In larger production apps, splitting `main.py` from the configuration logic is essential to avoid circular dependencies and messy bootstrap code.

### The Lifespan Pattern
We use the FastAPI `lifespan` context manager to orchestrate the application's lifecycle:
1.  **Startup**: `setup_infrastructure()` is called. It initializes the main Redis client (`init_redis`) and all ARQ pools (`create_redis_queue_pools`).
2.  **Yield**: The application starts receiving requests.
3.  **Shutdown**: `teardown_infrastructure()` is called, ensuring all databases and redis connections are closed gracefully.

### Why `queue.py` holds placeholders?
To allow routes and services to import the queue pools without importing the heavy initialization logic in `setup.py`, we store the pool objects as attributes in `app/core/queue.py`. During startup, `setup.py` populates these placeholders.

---

## 3. Multi-Worker & Multi-Queue (ARQ)
The system is built for heavy-duty background processing by isolating workloads into specialized worker processes.

### Logical DB Isolation
We utilize Redis database indices to ensure total isolation between queues:
- **DB 1 (Base Queue)**: Used for general maintenance jobs or lightweight logging.
- **DB 2 (Email Queue)**: Reserved for mission-critical notifications.

### Specialized Worker Configuration
Each worker process has its own settings in `app/core/worker/`. This is critical for **Scalability**:
- You can run multiple instances of the `email_worker` without them competing for the same jobs as the `base_worker`.
- Each worker only loads the functions it is responsible for, reducing memory overhead.

---

## 4. How to add a new Queue ➕
To extend the system with a new queue (e.g., a "report" queue):

### Step 1: Define the Job
Create the task function in `app/workers/jobs.py`:
```python
async def generate_report(ctx, report_id: int):
    # Logic for heavy report generation
    return f"Report {report_id} generated"
```

### Step 2: Create Worker Settings
Create `app/core/worker/report_settings.py`. This defines the worker's unique identity:
```python
from arq.connections import RedisSettings
from app.core.config import settings
from app.workers.jobs import generate_report

class WorkerSettings:
    functions = [generate_report]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    redis_settings.database = 3  # Important: Use a unique DB index
```

### Step 3: Update Global State Container
Add the pool placeholder to `app/core/queue.py`:
```python
# app/core/queue.py
report_pool: ArqRedis | None = None
```

### Step 4: Register in Infrastructure Setup
Import the new settings and add the pool to `app/core/setup.py`:
```python
# app/core/setup.py
from app.core.worker.report_settings import WorkerSettings as ReportSettings

async def create_redis_queue_pools() -> None:
    # ...
    queue.report_pool = await create_pool(ReportSettings.redis_settings)
```

### Step 5: Create Run Script
Create `run_report_worker.py`:
```python
import asyncio
from arq import run_worker
from app.core.worker.report_settings import WorkerSettings

if __name__ == "__main__":
    asyncio.run(run_worker(WorkerSettings))
```

### Step 6: Trigger the Job
From any route or service:
```python
from app.core import queue
await queue.report_pool.enqueue_job("generate_report", report_id=123)
```

---

## 5. Development & Deployment
- **Docker Compose**: Automatically starts the API and both workers as separate containers.
- **Migrations**: Uses `alembic` with an async environment to manage PostgreSQL changes.
- **Scaling**: In production, you can scale each worker service independently in your orchestrator (e.g., Kubernetes or Docker Swarm).
