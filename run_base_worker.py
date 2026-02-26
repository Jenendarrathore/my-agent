import asyncio
from arq import run_worker
from app.core.worker.base_settings import WorkerSettings

if __name__ == "__main__":
    asyncio.run(run_worker(WorkerSettings))
