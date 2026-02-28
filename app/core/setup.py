from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import APIRouter, FastAPI
from arq.connections import RedisSettings, create_pool
from fastapi import APIRouter, FastAPI
from app.core.config import settings
from app.core.redis import init_redis, close_redis
from app.core import queue
from app.core.worker.base_settings import WorkerSettings as BaseWorkerSettings
from app.core.worker.email_settings import WorkerSettings as EmailWorkerSettings


async def create_redis_queue_pools() -> None:
    """Initialize all ARQ pools with logical database isolation."""
    # Pool for base queue (DB 1)
    queue.base_pool = await create_pool(BaseWorkerSettings.redis_settings)
    
    # Pool for email queue (DB 2)
    queue.email_pool = await create_pool(EmailWorkerSettings.redis_settings)


async def close_redis_queue_pools() -> None:
    """Close all ARQ pools gracefully."""
    if queue.base_pool:
        await queue.base_pool.close()
        queue.base_pool = None
    if queue.email_pool:
        await queue.email_pool.close()
        queue.email_pool = None


async def setup_infrastructure():
    """Initialize all infrastructure components."""
    await init_redis()
    await create_redis_queue_pools()


async def teardown_infrastructure():
    """Close all infrastructure connections."""
    await close_redis_queue_pools()
    await close_redis()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    """Application lifespan context manager."""
    await setup_infrastructure()
    yield
    await teardown_infrastructure()


def create_application(router: APIRouter, **kwargs: Any) -> FastAPI:
    """Creates and configures a FastAPI application instance."""
    
    # Merge default metadata with provided kwargs
    app_configs = {
        "title": "FastAPI Boilerplate",
        "description": "A production-ready FastAPI boilerplate with logical worker queues.",
        "version": "1.0.0",
        "lifespan": lifespan,
    }
    app_configs.update(kwargs)
    
    application = FastAPI(**app_configs)
    
    # Enable CORS
    from fastapi.middleware.cors import CORSMiddleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include the main router
    application.include_router(router)
    
    return application
