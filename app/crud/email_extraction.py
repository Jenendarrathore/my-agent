from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.email_extraction import EmailExtraction
from app.schemas.email_extraction import EmailExtractionCreate


async def create_email_extraction(db: AsyncSession, obj_in: EmailExtractionCreate) -> EmailExtraction:
    db_obj = EmailExtraction(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def get_email_extraction(db: AsyncSession, id: int) -> Optional[EmailExtraction]:
    result = await db.execute(select(EmailExtraction).where(EmailExtraction.id == id))
    return result.scalars().first()


async def get_extractions_by_email(db: AsyncSession, email_id: int) -> List[EmailExtraction]:
    result = await db.execute(select(EmailExtraction).where(EmailExtraction.email_id == email_id))
    return list(result.scalars().all())


async def delete_email_extraction(db: AsyncSession, id: int) -> bool:
    db_obj = await get_email_extraction(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
        return True
    return False
