from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.llm_transaction import LLMTransaction
from app.schemas.llm_transaction import LLMTransactionCreate


async def create_llm_transaction(db: AsyncSession, obj_in: LLMTransactionCreate) -> LLMTransaction:
    db_obj = LLMTransaction(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def get_llm_transaction(db: AsyncSession, id: int) -> Optional[LLMTransaction]:
    result = await db.execute(select(LLMTransaction).where(LLMTransaction.id == id))
    return result.scalars().first()


async def get_llm_transactions_by_job(db: AsyncSession, job_id: int) -> List[LLMTransaction]:
    result = await db.execute(select(LLMTransaction).where(LLMTransaction.job_id == job_id))
    return list(result.scalars().all())


async def delete_llm_transaction(db: AsyncSession, id: int) -> bool:
    db_obj = await get_llm_transaction(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
        return True
    return False
