from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.email_connection import EmailConnection
from app.schemas.email_connection import EmailConnectionCreate, EmailConnectionUpdate


async def create_email_connection(db: AsyncSession, obj_in: EmailConnectionCreate) -> EmailConnection:
    db_obj = EmailConnection(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def get_email_connection(db: AsyncSession, id: int) -> Optional[EmailConnection]:
    result = await db.execute(select(EmailConnection).where(EmailConnection.id == id))
    return result.scalars().first()


async def get_email_connections_by_user(db: AsyncSession, user_id: int) -> List[EmailConnection]:
    result = await db.execute(select(EmailConnection).where(EmailConnection.user_id == user_id))
    return list(result.scalars().all())


async def update_email_connection(
    db: AsyncSession, db_obj: EmailConnection, obj_in: EmailConnectionUpdate
) -> EmailConnection:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_email_connection(db: AsyncSession, id: int) -> bool:
    db_obj = await get_email_connection(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
        return True
    return False
