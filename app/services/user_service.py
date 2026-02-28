from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user as crud
from app.schemas.user import UserCreate, UserUpdate, UserResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_in: UserCreate) -> UserResponse:
        db_obj = await crud.create_user(self.db, user_in)
        return UserResponse.model_validate(db_obj)

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        db_obj = await crud.get_user(self.db, user_id)
        return UserResponse.model_validate(db_obj) if db_obj else None

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        db_obj = await crud.get_user_by_email(self.db, email)
        return UserResponse.model_validate(db_obj) if db_obj else None

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        db_objs = await crud.get_users(self.db, skip, limit)
        return [UserResponse.model_validate(obj) for obj in db_objs]

    async def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[UserResponse]:
        db_obj = await crud.get_user(self.db, user_id)
        if not db_obj:
            return None
        updated_obj = await crud.update_user(self.db, db_user=db_obj, user_in=user_in)
        return UserResponse.model_validate(updated_obj)

    async def delete_user(self, user_id: int) -> bool:
        return await crud.delete_user(self.db, user_id)
