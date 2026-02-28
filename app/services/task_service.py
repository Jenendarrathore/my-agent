from typing import Optional
from app.core import queue

class TaskService:
    @staticmethod
    async def enqueue_email_fetch(user_id: int, provider: str = "gmail", limit: int = 20, account_id: Optional[int] = None):
        """Enqueue an email fetch job to the email pool."""
        if not queue.email_pool:
            raise RuntimeError("Email queue pool is not initialized. Ensure the application is running.")
        
        await queue.email_pool.enqueue_job(
            "run_email_fetch", 
            user_id=user_id, 
            provider=provider, 
            limit=limit,
            account_id=account_id
        )

    @staticmethod
    async def enqueue_email_extraction(batch_size: int = 10):
        """Enqueue an email extraction job to the email pool."""
        if not queue.email_pool:
            raise RuntimeError("Email queue pool is not initialized. Ensure the application is running.")
        
        await queue.email_pool.enqueue_job(
            "run_email_extraction", 
            batch_size=batch_size
        )
