from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


async def create_job(db: AsyncSession, obj_in: JobCreate) -> Job:
    db_obj = Job(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def get_job(db: AsyncSession, id: int) -> Optional[Job]:
    result = await db.execute(select(Job).where(Job.id == id))
    return result.scalars().first()


async def get_jobs(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    status: Optional[str] = None,
    job_type: Optional[str] = None
) -> List[Job]:
    query = select(Job)
    if status:
        query = query.where(Job.status == status)
    if job_type:
        query = query.where(Job.job_type == job_type)
    
    query = query.offset(skip).limit(limit).order_by(Job.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def update_job(db: AsyncSession, db_obj: Job, obj_in: JobUpdate) -> Job:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_job(db: AsyncSession, id: int) -> bool:
    db_obj = await get_job(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
        return True
    return False
