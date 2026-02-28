from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import email as crud
from app.schemas.email import EmailCreate, EmailUpdate, EmailRead


class EmailService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_email(self, email_in: EmailCreate) -> EmailRead:
        db_obj = await crud.create_email(self.db, email_in)
        return EmailRead.model_validate(db_obj)

    async def get_email(self, id: int) -> Optional[EmailRead]:
        db_obj = await crud.get_email(self.db, id)
        return EmailRead.model_validate(db_obj) if db_obj else None

    async def get_email_by_provider_id(self, user_id: int, provider: str, provider_message_id: str) -> Optional[EmailRead]:
        db_obj = await crud.get_email_by_provider_id(self.db, user_id, provider, provider_message_id)
        return EmailRead.model_validate(db_obj) if db_obj else None

    async def list_user_emails(self, user_id: int, skip: int = 0, limit: int = 100) -> List[EmailRead]:
        db_objs = await crud.get_emails_by_user(self.db, user_id, skip, limit)
        return [EmailRead.model_validate(obj) for obj in db_objs]

    async def update_email(self, id: int, email_in: EmailUpdate) -> Optional[EmailRead]:
        db_obj = await crud.get_email(self.db, id)
        if not db_obj:
            return None
        updated_obj = await crud.update_email(self.db, db_obj, email_in)
        return EmailRead.model_validate(updated_obj)

    async def delete_email(self, id: int) -> bool:
        return await crud.delete_email(self.db, id)
