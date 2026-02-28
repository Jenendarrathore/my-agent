from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import connected_account as crud
from app.schemas.connected_account import ConnectedAccountCreate, ConnectedAccountUpdate, ConnectedAccountResponse


from app.models.connected_account import ConnectedAccount


class ConnectedAccountService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_account(self, account_in: ConnectedAccountCreate, user_id: int) -> ConnectedAccountResponse:
        db_obj = await crud.create_connected_account(self.db, account_in, user_id)
        return ConnectedAccountResponse.model_validate(db_obj)

    async def get_account(self, account_id: int) -> Optional[ConnectedAccountResponse]:
        db_obj = await crud.get_connected_account(self.db, account_id)
        return ConnectedAccountResponse.model_validate(db_obj) if db_obj else None

    async def get_account_db(self, account_id: int) -> Optional[ConnectedAccount]:
        """Internal use only: returns SQLAlchemy model with sensitive tokens."""
        return await crud.get_connected_account(self.db, account_id)

    async def list_user_accounts(self, user_id: int) -> List[ConnectedAccountResponse]:
        db_objs = await crud.get_connected_accounts_by_user(self.db, user_id)
        return [ConnectedAccountResponse.model_validate(obj) for obj in db_objs]

    async def list_user_accounts_db(self, user_id: int) -> List[ConnectedAccount]:
        """Internal use only: returns SQLAlchemy models with sensitive tokens."""
        return await crud.get_connected_accounts_by_user(self.db, user_id)

    async def update_account(self, account_id: int, account_in: ConnectedAccountUpdate) -> Optional[ConnectedAccountResponse]:
        db_obj = await crud.get_connected_account(self.db, account_id)
        if not db_obj:
            return None
        updated_obj = await crud.update_connected_account(self.db, db_obj, account_in)
        return ConnectedAccountResponse.model_validate(updated_obj)

    async def delete_account(self, account_id: int) -> bool:
        return await crud.delete_connected_account(self.db, account_id)
