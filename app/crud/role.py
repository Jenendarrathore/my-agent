from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


class CRUDRole:
    async def get(self, db: AsyncSession, id: int) -> Optional[Role]:
        result = await db.execute(select(Role).where(Role.id == id))
        return result.scalars().first()

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Role]:
        result = await db.execute(select(Role).where(Role.name == name))
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Role]:
        result = await db.execute(select(Role).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: RoleCreate) -> Role:
        db_obj = Role(name=obj_in.name)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Role, obj_in: RoleUpdate
    ) -> Role:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[Role]:
        db_obj = await self.get(db, id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj


role = CRUDRole()
