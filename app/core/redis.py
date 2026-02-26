import redis.asyncio as redis
from app.core.config import settings
from typing import AsyncGenerator

# Create a global Redis client instance (will be initialized on startup)
redis_client: redis.Redis | None = None

async def init_redis() -> None:
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(settings.REDIS_URL, decode_responses=True)

async def close_redis() -> None:
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    if redis_client is None:
        await init_redis()
    assert redis_client is not None
    yield redis_client
