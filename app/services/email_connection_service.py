from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import email_connection as crud
from app.schemas.email_connection import EmailConnectionCreate, EmailConnectionUpdate, EmailConnectionRead


class EmailConnectionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_connection(self, connection_in: EmailConnectionCreate) -> EmailConnectionRead:
        db_obj = await crud.create_email_connection(self.db, connection_in)
        return EmailConnectionRead.model_validate(db_obj)

    async def get_connection(self, id: int) -> Optional[EmailConnectionRead]:
        db_obj = await crud.get_email_connection(self.db, id)
        return EmailConnectionRead.model_validate(db_obj) if db_obj else None

    async def list_user_connections(self, user_id: int) -> List[EmailConnectionRead]:
        db_objs = await crud.get_email_connections_by_user(self.db, user_id)
        return [EmailConnectionRead.model_validate(obj) for obj in db_objs]

    async def update_connection(self, id: int, connection_in: EmailConnectionUpdate) -> Optional[EmailConnectionRead]:
        db_obj = await crud.get_email_connection(self.db, id)
        if not db_obj:
            return None
        updated_obj = await crud.update_email_connection(self.db, db_obj, connection_in)
        return EmailConnectionRead.model_validate(updated_obj)

    async def delete_connection(self, id: int) -> bool:
        return await crud.delete_email_connection(self.db, id)
