---
sidebar_position: 5
sidebar_label: "Adding a New Worker"
---

# 📋 SOP: Adding a New Worker

## When to Use

Use this SOP when you need to create a completely new, logically isolated queue (e.g., a "high-priority" queue, an "ai-processing" queue, or a "webhook" queue) using a distinct Redis database.

If you just need to add a new job to an existing queue (like the `base` or `email` queue), refer to the [Adding a New Background Job](adding-new-job.md) SOP instead.

---

## Step 1: Assign a Redis Database

ARQ uses logical Redis databases to isolate queues.
1. Check `app/core/worker/` to see which databases are currently in use.
   - Example Defaults: DB 1 = Base Worker, DB 2 = Email Worker.
2. Pick the next available database index (e.g., `3`).

---

## Step 2: Create the ARQ Task Functions

Create or identify the task functions your worker will run. Usually, these go in `app/workers/jobs.py` (or a dedicated file if it's a completely distinct domain).

```python
# app/workers/jobs.py

async def run_my_new_task(ctx, user_id: int):
    """ARQ Task: Example for the new worker."""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Running new task for user {user_id}")
    # ... logic here ...
```

---

## Step 3: Create the Worker Settings File

Create a new file in `app/core/worker/`, for example `app/core/worker/my_queue_settings.py`.

```python
from arq.connections import RedisSettings
from app.core.config import settings
from app.core.setup import create_redis_queue_pools
from app.core.database import Base, engine
from app.workers.jobs import run_my_new_task

async def startup(ctx):
    """Actions to run on worker startup."""
    print("Starting my new queue worker...")
    # Optional: ensure DB tables exist, init connections, etc.

async def shutdown(ctx):
    """Actions to run on worker shutdown."""
    print("Shutting down my new queue worker...")

class WorkerSettings:
    """
    ARQ settings for the new queue worker.
    Uses a dedicated Redis Database to isolate this queue.
    """
    # 1. Register the functions this worker can execute
    functions = [run_my_new_task]
    
    # 2. Configure the Redis connection
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    
    # 3. SET THE UNIQUE DATABASE INDEX HERE
    redis_settings.database = 3  
    
    # 4. Hook up lifecycle events
    on_startup = startup
    on_shutdown = shutdown
```

---

## Step 4: Create a Global Connection Pool Placeholder

To enqueue jobs to this new worker from your API, you need a connection pool. 

Edit `app/core/queue.py` and add a new pool variable:

```python
from arq.connections import ArqRedis

base_pool: ArqRedis | None = None
email_pool: ArqRedis | None = None
my_new_pool: ArqRedis | None = None  # Add this
```

---

## Step 5: Initialize the Pool on App Startup

Edit `app/core/setup.py` to initialize your new pool when the FastAPI application starts.

First, import your worker settings:
```python
from app.core.worker.my_queue_settings import WorkerSettings as MyQueueWorkerSettings
```

Then, update the `create_redis_queue_pools` function:
```python
async def create_redis_queue_pools() -> None:
    # Existing pools...
    queue.base_pool = await create_pool(BaseWorkerSettings.redis_settings)
    queue.email_pool = await create_pool(EmailWorkerSettings.redis_settings)
    
    # Add your new pool
    queue.my_new_pool = await create_pool(MyQueueWorkerSettings.redis_settings)
```

---

## Step 6: Create Enqueue Methods

Update `app/services/task_service.py` to provide a clean interface for enqueueing jobs to your new worker.

```python
from app.core import queue

class TaskService:
    # ... existing methods ...
    
    @staticmethod
    async def enqueue_my_new_task(user_id: int):
        if not queue.my_new_pool:
            raise RuntimeError("my_new_pool is not initialized")
            
        await queue.my_new_pool.enqueue_job("run_my_new_task", user_id=user_id)
```

---

## Step 7: Create a Runner Script (Optional but Recommended)

For convenience in local development, create a script in the root directory (e.g., `run_my_new_worker.py`) to easily launch the worker:

```python
import subprocess
import sys

def main():
    try:
        # Note the path to the WorkerSettings class you created in Step 3
        cmd = [sys.executable, "-m", "arq", "app.core.worker.my_queue_settings.WorkerSettings"]
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("Worker stopped.")
    except Exception as e:
        print(f"Error running worker: {e}")

if __name__ == "__main__":
    main()
```

---

## Step 8: Update Docker Compose

If you are using Docker, you need to add this new worker as a separate service in your `docker-compose.yml` so it runs alongside the API and other workers:

```yaml
services:
  # ... api, db, redis, base_worker, email_worker ...

  my_new_worker:
    build: .
    command: arq app.core.worker.my_queue_settings.WorkerSettings
    depends_on:
      - redis
      - db
    env_file:
      - .env
```

---

## Step 9: Run the Worker

You must have the worker running as a separate process to process the jobs.

Locally, open a new terminal using your virtual environment:

```bash
# Using the ARQ CLI directly
arq app.core.worker.my_queue_settings.WorkerSettings

# OR using the runner script you created:
python run_my_new_worker.py
```

If testing via Docker Compose:
```bash
docker-compose up -d my_new_worker
```
