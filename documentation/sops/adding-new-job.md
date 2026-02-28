# 📋 SOP: Adding a New Background Job

## When to Use

Use this SOP when you need to create a new background task that runs asynchronously via ARQ workers.

---

## Step 1: Decide the Queue

| Queue | Redis DB | Worker | Use For |
|-------|----------|--------|---------|
| Base | DB 1 | `base_settings.WorkerSettings` | General-purpose tasks |
| Email | DB 2 | `email_settings.WorkerSettings` | Email/notification tasks |

---

## Step 2: Create the Job Class

Create `app/jobs/<job_name>.py`:

```python
from typing import Any, Dict
from app.jobs.base import BaseJob
import logging

logger = logging.getLogger(__name__)


class MyNewJob(BaseJob):
    """
    Description of what this job does.
    """

    async def run(self) -> Dict[str, Any]:
        # Access input via self.input_payload
        user_id = self.input_payload.get("user_id")
        some_param = self.input_payload.get("some_param", "default")
        
        # Access DB via self.db (AsyncSession)
        # Access parent job record via self.job_record (after before_run)
        
        logger.info(f"Running MyNewJob for user {user_id}")
        
        # ... your logic here ...
        
        # Return result as dict (stored in job.output_payload)
        return {
            "processed": 42,
            "user_id": user_id
        }
    
    # Optional: override lifecycle hooks
    async def before_run(self, job_record):
        await super().before_run(job_record)
        # Custom pre-run logic
    
    async def after_run(self, result):
        await super().after_run(result)
        # Custom post-run logic
    
    async def on_failure(self, error):
        await super().on_failure(error)
        # Custom error handling (e.g., send alert)
```

---

## Step 3: Register in `app/jobs/__init__.py`

```python
from .my_new_job import MyNewJob

__all__ = [
    # ... existing
    "MyNewJob",
]
```

---

## Step 4: Create the ARQ Task Function

Add to `app/workers/jobs.py`:

```python
from app.jobs import MyNewJob

async def run_my_new_job(ctx, user_id: int, some_param: str = "default"):
    """ARQ Task: Description."""
    async with AsyncSessionLocal() as db:
        runner = JobRunner(db)
        payload = {"user_id": user_id, "some_param": some_param}
        await runner.run_job(
            MyNewJob, 
            "MY_NEW_JOB",       # job_type stored in DB
            payload, 
            triggered_by="system",
            user_id=user_id
        )
```

---

## Step 5: Register with Worker Settings

Add the function to the appropriate worker's `functions` list:

**For Email Worker** (`app/core/worker/email_settings.py`):
```python
from app.workers.jobs import run_my_new_job

class WorkerSettings:
    functions = [send_email, send_otp_email, run_email_fetch, run_email_extraction, run_my_new_job]
    # ...
```

**For Base Worker** (`app/core/worker/base_settings.py`):
```python
from app.workers.jobs import run_my_new_job

class WorkerSettings:
    functions = [sample_task, run_my_new_job]
    # ...
```

---

## Step 6: Create Enqueue Method in TaskService

Add to `app/services/task_service.py`:

```python
@staticmethod
async def enqueue_my_new_job(user_id: int, some_param: str = "default"):
    """Enqueue my new job."""
    if not queue.email_pool:  # or queue.base_pool depending on queue
        raise RuntimeError("Queue pool not initialized")
    
    await queue.email_pool.enqueue_job(
        "run_my_new_job",
        user_id=user_id,
        some_param=some_param
    )
```

---

## Step 7: Add API Trigger Endpoint (Optional)

Add to `app/api/v1/jobs.py` (or relevant router):

```python
@router.post("/trigger/my-job", status_code=status.HTTP_202_ACCEPTED)
async def trigger_my_new_job(
    some_param: str = "default",
    current_user: User = Depends(get_current_user)
):
    """Trigger my new background job."""
    await TaskService.enqueue_my_new_job(
        user_id=current_user.id, 
        some_param=some_param
    )
    return {"message": "Job enqueued"}
```

---

## Step 8: Restart Worker

Workers need to be restarted to pick up new task functions:

```bash
# Stop and restart the relevant worker
./venv/bin/arq app.core.worker.email_settings.WorkerSettings
```

---

## Files Modified Checklist

| File | Action |
|------|--------|
| `app/jobs/<job_name>.py` | **Create** — Job class |
| `app/jobs/__init__.py` | **Modify** — Register import |
| `app/workers/jobs.py` | **Modify** — Add ARQ task function |
| `app/core/worker/<worker>_settings.py` | **Modify** — Add to `functions` |
| `app/services/task_service.py` | **Modify** — Add enqueue method |
| `app/api/v1/jobs.py` | **Modify** — Add trigger endpoint (optional) |
