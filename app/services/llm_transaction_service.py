from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import llm_transaction as crud
from app.schemas.llm_transaction import LLMTransactionCreate, LLMTransactionRead


class LLMTransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_transaction(self, transaction_in: LLMTransactionCreate) -> LLMTransactionRead:
        db_obj = await crud.create_llm_transaction(self.db, transaction_in)
        return LLMTransactionRead.model_validate(db_obj)

    async def get_transaction(self, id: int) -> Optional[LLMTransactionRead]:
        db_obj = await crud.get_llm_transaction(self.db, id)
        return LLMTransactionRead.model_validate(db_obj) if db_obj else None

    async def list_job_transactions(self, job_id: int) -> List[LLMTransactionRead]:
        db_objs = await crud.get_llm_transactions_by_job(self.db, job_id)
        return [LLMTransactionRead.model_validate(obj) for obj in db_objs]

    async def delete_transaction(self, id: int) -> bool:
        return await crud.delete_llm_transaction(self.db, id)
