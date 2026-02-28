from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.email import Email
from app.schemas.email import EmailCreate, EmailUpdate


async def create_email(db: AsyncSession, obj_in: EmailCreate) -> Email:
    db_obj = Email(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def get_email(db: AsyncSession, id: int) -> Optional[Email]:
    result = await db.execute(select(Email).where(Email.id == id))
    return result.scalars().first()


async def get_email_by_provider_id(db: AsyncSession, provider: str, provider_message_id: str) -> Optional[Email]:
    result = await db.execute(
        select(Email).where(Email.provider == provider, Email.provider_message_id == provider_message_id)
    )
    return result.scalars().first()


async def get_emails_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[Email]:
    result = await db.execute(
        select(Email)
        .where(Email.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def update_email(db: AsyncSession, db_obj: Email, obj_in: EmailUpdate) -> Email:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_email(db: AsyncSession, id: int) -> bool:
    db_obj = await get_email(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
        return True
    return False
