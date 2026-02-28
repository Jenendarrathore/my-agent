from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    db_user = User(
        name=user_in.name,
        username=user_in.username,
        primary_email=user_in.primary_email,
        password_hash=user_in.password,  # In real app, hash this!
        role_id=getattr(user_in, 'role_id', 2) # Default to 2 (user) for now
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.primary_email == email))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())


async def update_user(db: AsyncSession, db_user: User, user_in: UserUpdate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    if "password" in user_data:
        user_data["password_hash"] = user_data.pop("password")
    
    for field, value in user_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False
