from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import category as crud
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_category(self, category_in: CategoryCreate, user_id: int) -> CategoryResponse:
        db_obj = await crud.create_category(self.db, category_in, user_id)
        return CategoryResponse.model_validate(db_obj)

    async def get_category(self, category_id: int) -> Optional[CategoryResponse]:
        db_obj = await crud.get_category(self.db, category_id)
        return CategoryResponse.model_validate(db_obj) if db_obj else None

    async def list_user_categories(self, user_id: int) -> List[CategoryResponse]:
        db_objs = await crud.get_categories_by_user(self.db, user_id)
        return [CategoryResponse.model_validate(obj) for obj in db_objs]

    async def get_category_by_name(self, user_id: int, name: str) -> Optional[CategoryResponse]:
        db_obj = await crud.get_category_by_name(self.db, user_id, name)
        return CategoryResponse.model_validate(db_obj) if db_obj else None

    async def update_category(self, category_id: int, category_in: CategoryUpdate) -> Optional[CategoryResponse]:
        db_obj = await crud.get_category(self.db, category_id)
        if not db_obj:
            return None
        updated_obj = await crud.update_category(self.db, db_obj, category_in)
        return CategoryResponse.model_validate(updated_obj)

    async def delete_category(self, category_id: int) -> bool:
        return await crud.delete_category(self.db, category_id)
