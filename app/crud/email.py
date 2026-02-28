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


async def get_email_by_provider_id(db: AsyncSession, user_id: int, provider: str, provider_message_id: str) -> Optional[Email]:
    result = await db.execute(
        select(Email).where(
            Email.user_id == user_id,
            Email.provider == provider, 
            Email.provider_message_id == provider_message_id
        )
    )
    return result.scalars().first()


async def get_emails_by_user(db: AsyncSession, user_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Email]:
    query = select(Email)
    if user_id is not None:
        query = query.where(Email.user_id == user_id)
    
    query = query.offset(skip).limit(limit).order_by(Email.received_at.desc())
    result = await db.execute(query)
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
