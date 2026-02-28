from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import CategoryService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)
    return await service.create_category(category_in=category_in, user_id=current_user.id)


@router.get("/", response_model=List[CategoryResponse])
async def read_categories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)
    return await service.list_user_categories(user_id=current_user.id)


@router.get("/{category_id}", response_model=CategoryResponse)
async def read_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)
    category = await service.get_category(category_id=category_id)
    if not category or category.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, 
    category_in: CategoryUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)
    category = await service.get_category(category_id=category_id)
    if not category or category.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Category not found")
    return await service.update_category(category_id=category_id, category_in=category_in)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CategoryService(db)
    category = await service.get_category(category_id=category_id)
    if not category or category.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Category not found")
        
    success = await service.delete_category(category_id=category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return None

