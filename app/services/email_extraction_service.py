from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import email_extraction as crud
from app.schemas.email_extraction import EmailExtractionCreate, EmailExtractionRead


class EmailExtractionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_extraction(self, extraction_in: EmailExtractionCreate) -> EmailExtractionRead:
        db_obj = await crud.create_email_extraction(self.db, extraction_in)
        return EmailExtractionRead.model_validate(db_obj)

    async def get_extraction(self, id: int) -> Optional[EmailExtractionRead]:
        db_obj = await crud.get_email_extraction(self.db, id)
        return EmailExtractionRead.model_validate(db_obj) if db_obj else None

    async def list_email_extractions(self, email_id: int) -> List[EmailExtractionRead]:
        db_objs = await crud.get_extractions_by_email(self.db, email_id)
        return [EmailExtractionRead.model_validate(obj) for obj in db_objs]

    async def delete_extraction(self, id: int) -> bool:
        return await crud.delete_email_extraction(self.db, id)
