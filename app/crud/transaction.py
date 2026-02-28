from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


async def create_transaction(db: AsyncSession, transaction_in: TransactionCreate, user_id: int) -> Transaction:
    db_transaction = Transaction(
        **transaction_in.model_dump(exclude={"user_id"}),
        user_id=user_id
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction


async def get_transaction(db: AsyncSession, transaction_id: int) -> Optional[Transaction]:
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    return result.scalars().first()


async def get_transactions_by_user(
    db: AsyncSession, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[Transaction]:
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.occurred_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def update_transaction(
    db: AsyncSession, 
    db_transaction: Transaction, 
    transaction_in: TransactionUpdate
) -> Transaction:
    transaction_data = transaction_in.model_dump(exclude_unset=True)
    for field, value in transaction_data.items():
        setattr(db_transaction, field, value)
    
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction


async def delete_transaction(db: AsyncSession, transaction_id: int) -> bool:
    db_transaction = await get_transaction(db, transaction_id)
    if db_transaction:
        await db.delete(db_transaction)
        await db.commit()
        return True
    return False
