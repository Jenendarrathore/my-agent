from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import job as crud
from app.schemas.job import JobCreate, JobUpdate, JobRead


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_job(self, job_in: JobCreate) -> JobRead:
        db_obj = await crud.create_job(self.db, job_in)
        return JobRead.model_validate(db_obj)

    async def get_job(self, id: int) -> Optional[JobRead]:
        db_obj = await crud.get_job(self.db, id)
        return JobRead.model_validate(db_obj) if db_obj else None

    async def list_jobs(self, skip: int = 0, limit: int = 100) -> List[JobRead]:
        db_objs = await crud.get_jobs(self.db, skip, limit)
        return [JobRead.model_validate(obj) for obj in db_objs]

    async def update_job(self, id: int, job_in: JobUpdate) -> Optional[JobRead]:
        db_obj = await crud.get_job(self.db, id)
        if not db_obj:
            return None
        updated_obj = await crud.update_job(self.db, db_obj, job_in)
        return JobRead.model_validate(updated_obj)

    async def delete_job(self, id: int) -> bool:
        return await crud.delete_job(self.db, id)
