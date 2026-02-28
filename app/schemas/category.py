from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.category import CategoryType


class CategoryBase(BaseModel):
    name: str
    type: CategoryType = CategoryType.expense
    is_system: bool = False


class CategoryCreate(CategoryBase):
    user_id: Optional[int] = None  # Usually taken from auth context


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None
    is_system: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
