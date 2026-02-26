from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

async def create_user(db: AsyncSession, user_in: UserCreate) -> UserRead:
    new_user = User(name=user_in.name, email=user_in.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserRead.from_orm(new_user)

async def get_user(db: AsyncSession, user_id: int) -> UserRead:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise ValueError("User not found")
    return UserRead.from_orm(user)

async def list_users(db: AsyncSession) -> List[UserRead]:
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [UserRead.from_orm(u) for u in users]
