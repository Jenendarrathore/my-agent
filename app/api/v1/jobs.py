from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.job import JobCreate, JobUpdate, JobRead
from app.services.job_service import JobService
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.task_service import TaskService
from typing import Optional

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/trigger/fetch", status_code=status.HTTP_202_ACCEPTED)
async def trigger_email_fetch(
    provider: str = "gmail",
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """Trigger a background job to fetch emails for the current user."""
    await TaskService.enqueue_email_fetch(user_id=current_user.id, provider=provider, limit=limit)
    return {"message": "Email fetch job enqueued"}


@router.post("/trigger/extract", status_code=status.HTTP_202_ACCEPTED)
async def trigger_email_extraction(
    batch_size: int = 10,
    current_user: User = Depends(get_current_user)
):
    """Trigger a background job to extract data from all pending emails."""
    await TaskService.enqueue_email_extraction(batch_size=batch_size)
    return {"message": "Email extraction job enqueued"}


@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Jobs might be system-wide or triggered by any user, for now allow all auth users
    service = JobService(db)
    return await service.create_job(job_in)


@router.get("/", response_model=List[JobRead])
async def read_jobs(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    job_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = JobService(db)
    return await service.list_jobs(skip=skip, limit=limit, status=status, job_type=job_type)


@router.get("/{job_id}", response_model=JobRead)
async def read_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = JobService(db)
    job = await service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.patch("/{job_id}", response_model=JobRead)
async def update_job(
    job_id: int,
    job_in: JobUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = JobService(db)
    job = await service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return await service.update_job(job_id, job_in)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = JobService(db)
    job = await service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    success = await service.delete_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return None
