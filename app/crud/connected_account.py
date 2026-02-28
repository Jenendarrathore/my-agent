from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.connected_account import ConnectedAccount
from app.schemas.connected_account import ConnectedAccountCreate, ConnectedAccountUpdate


async def create_connected_account(
    db: AsyncSession, 
    account_in: ConnectedAccountCreate, 
    user_id: int
) -> ConnectedAccount:
    db_account = ConnectedAccount(
        **account_in.model_dump(exclude={"user_id"}),
        user_id=user_id
    )
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account


async def get_connected_account(db: AsyncSession, account_id: int) -> Optional[ConnectedAccount]:
    result = await db.execute(select(ConnectedAccount).where(ConnectedAccount.id == account_id))
    return result.scalars().first()


async def get_connected_accounts_by_user(db: AsyncSession, user_id: int) -> List[ConnectedAccount]:
    result = await db.execute(select(ConnectedAccount).where(ConnectedAccount.user_id == user_id))
    return list(result.scalars().all())


async def update_connected_account(
    db: AsyncSession, 
    db_account: ConnectedAccount, 
    account_in: ConnectedAccountUpdate
) -> ConnectedAccount:
    account_data = account_in.model_dump(exclude_unset=True)
    for field, value in account_data.items():
        setattr(db_account, field, value)
    
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account


async def delete_connected_account(db: AsyncSession, account_id: int) -> bool:
    db_account = await get_connected_account(db, account_id)
    if db_account:
        await db.delete(db_account)
        await db.commit()
        return True
    return False
