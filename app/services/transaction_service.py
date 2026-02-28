from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import transaction as crud
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse


class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_transaction(self, transaction_in: TransactionCreate, user_id: int) -> TransactionResponse:
        db_obj = await crud.create_transaction(self.db, transaction_in, user_id)
        return TransactionResponse.model_validate(db_obj)

    async def get_transaction(self, transaction_id: int) -> Optional[TransactionResponse]:
        db_obj = await crud.get_transaction(self.db, transaction_id)
        return TransactionResponse.model_validate(db_obj) if db_obj else None

    async def list_user_transactions(self, user_id: int, skip: int = 0, limit: int = 100) -> List[TransactionResponse]:
        db_objs = await crud.get_transactions_by_user(self.db, user_id, skip, limit)
        return [TransactionResponse.model_validate(obj) for obj in db_objs]

    async def update_transaction(self, transaction_id: int, transaction_in: TransactionUpdate) -> Optional[TransactionResponse]:
        db_obj = await crud.get_transaction(self.db, transaction_id)
        if not db_obj:
            return None
        updated_obj = await crud.update_transaction(self.db, db_obj, transaction_in)
        return TransactionResponse.model_validate(updated_obj)

    async def delete_transaction(self, transaction_id: int) -> bool:
        return await crud.delete_transaction(self.db, transaction_id)
