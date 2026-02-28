from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def create_category(db: AsyncSession, category_in: CategoryCreate, user_id: int) -> Category:
    db_category = Category(
        **category_in.model_dump(exclude={"user_id"}),
        user_id=user_id
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_category(db: AsyncSession, category_id: int) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalars().first()


async def get_categories_by_user(db: AsyncSession, user_id: int) -> List[Category]:
    result = await db.execute(select(Category).where(Category.user_id == user_id))
    return list(result.scalars().all())


async def get_category_by_name(db: AsyncSession, user_id: int, name: str) -> Optional[Category]:
    result = await db.execute(
        select(Category).where(Category.user_id == user_id, Category.name == name)
    )
    return result.scalars().first()


async def update_category(db: AsyncSession, db_category: Category, category_in: CategoryUpdate) -> Category:
    category_data = category_in.model_dump(exclude_unset=True)
    for field, value in category_data.items():
        setattr(db_category, field, value)
    
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_category(db: AsyncSession, category_id: int) -> bool:
    db_category = await get_category(db, category_id)
    if db_category:
        await db.delete(db_category)
        await db.commit()
        return True
    return False
