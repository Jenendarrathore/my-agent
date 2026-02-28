from arq.connections import RedisSettings
from app.core.config import settings
from app.workers.jobs import send_email, send_otp_email

async def startup(ctx):
    print("Email Worker starting...")

async def shutdown(ctx):
    print("Email Worker shutting down...")

class WorkerSettings:
    functions = [send_email, send_otp_email]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    # Use database 2 for email queue
    redis_settings.database = 2
    on_startup = startup
    on_shutdown = shutdown
