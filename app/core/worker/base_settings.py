from arq.connections import RedisSettings
from app.core.config import settings
from app.workers.jobs import sample_task

async def startup(ctx):
    print("Base Worker starting...")

async def shutdown(ctx):
    print("Base Worker shutting down...")

class WorkerSettings:
    functions = [sample_task]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    # Use database 1 for base queue
    redis_settings.database = 1
    on_startup = startup
    on_shutdown = shutdown
