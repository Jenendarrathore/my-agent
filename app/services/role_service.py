from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.role import role as role_crud
from app.schemas.role import RoleCreate, RoleUpdate
from app.models.role import Role


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_role(self, role_id: int) -> Optional[Role]:
        return await role_crud.get(self.db, id=role_id)

    async def get_role_by_name(self, name: str) -> Optional[Role]:
        return await role_crud.get_by_name(self.db, name=name)

    async def list_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        return await role_crud.get_multi(self.db, skip=skip, limit=limit)

    async def create_role(self, role_in: RoleCreate) -> Role:
        # Check if role already exists
        existing = await self.get_role_by_name(role_in.name)
        if existing:
            raise ValueError(f"Role with name '{role_in.name}' already exists.")
        
        db_obj = await role_crud.create(self.db, obj_in=role_in)
        return db_obj

    async def update_role(self, role_id: int, role_in: RoleUpdate) -> Role:
        db_obj = await self.get_role(role_id)
        if not db_obj:
            raise ValueError("Role not found.")
        
        if role_in.name:
            existing = await self.get_role_by_name(role_in.name)
            if existing and existing.id != role_id:
                raise ValueError(f"Role with name '{role_in.name}' already exists.")
        
        return await role_crud.update(self.db, db_obj=db_obj, obj_in=role_in)

    async def delete_role(self, role_id: int) -> bool:
        db_obj = await role_crud.remove(self.db, id=role_id)
        return db_obj is not None
