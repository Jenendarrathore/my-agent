import abc
import json
import logging
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job
from app.services.job_service import JobService
from app.schemas.job import JobUpdate

logger = logging.getLogger(__name__)

class BaseJob(abc.ABC):
    """
    Abstract base class for all jobs.
    Defines the lifecycle and required common functionality.
    """

    def __init__(self, db: AsyncSession, input_payload: Optional[Dict[str, Any]] = None):
        self.db = db
        self.input_payload = input_payload or {}
        self.job_record: Optional[Job] = None

    @abc.abstractmethod
    async def run(self) -> Any:
        """The main logic of the job."""
        pass

    async def before_run(self, job_record: Job) -> None:
        """Hook called before the run() method."""
        self.job_record = job_record
        logger.info(f"Starting job {job_record.id} ({job_record.job_type})")

    async def after_run(self, result: Any) -> None:
        """Hook called after successful run()."""
        logger.info(f"Job {self.job_record.id} completed successfully")

    async def on_failure(self, error: Exception) -> None:
        """Hook called if run() raises an exception."""
        logger.error(f"Job {self.job_record.id} failed: {str(error)}")
        logger.error(traceback.format_exc())


class JobRunner:
    """
    Orchestrator for job execution.
    Manages database state and job lifecycle.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.job_service = JobService(db)

    async def run_job(
        self, 
        job_class: Type[BaseJob], 
        job_type: str, 
        input_payload: Dict[str, Any],
        triggered_by: str = "SYSTEM",
        user_id: Optional[int] = None
    ) -> Job:
        """
        Creates a job record and executes the job lifecycle.
        """
        # 1. Create Job Record
        job_record = await self.job_service.create_job_raw(
            job_type=job_type,
            input_payload=input_payload,
            triggered_by=triggered_by,
            user_id=user_id,
            status="RUNNING"
        )
        await self.db.commit()
        await self.db.refresh(job_record)

        job_instance = job_class(self.db, input_payload)
        
        try:
            # 2. Lifecycle: before_run
            await job_instance.before_run(job_record)
            
            # Update start time
            await self.job_service.update_job(
                job_record.id, 
                JobUpdate(status="RUNNING", started_at=datetime.now(timezone.utc))
            )
            await self.db.commit()

            # 3. Lifecycle: run
            result = await job_instance.run()

            # 4. Lifecycle: after_run
            await job_instance.after_run(result)

            # 5. Mark SUCCESS
            await self.job_service.update_job(
                job_record.id, 
                JobUpdate(
                    status="SUCCESS", 
                    finished_at=datetime.now(timezone.utc),
                    output_payload=result if isinstance(result, dict) else {"result": str(result)}
                )
            )
            await self.db.commit()

        except Exception as e:
            # 6. Lifecycle: on_failure
            await job_instance.on_failure(e)

            # 7. Mark FAILED
            await self.job_service.update_job(
                job_record.id, 
                JobUpdate(
                    status="FAILED", 
                    finished_at=datetime.now(timezone.utc),
                    error_payload={"error": str(e), "traceback": traceback.format_exc()}
                )
            )
            await self.db.commit()
            
        return job_record
