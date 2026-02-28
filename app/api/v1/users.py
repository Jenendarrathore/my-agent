from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserService(db)
    # Optional: Check if current_user is admin
    db_user = await service.get_user_by_email(email=user_in.primary_email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )
    return await service.create_user(user_in=user_in)


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserService(db)
    return await service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserService(db)
    db_user = await service.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,     
    user_in: UserUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Logic: users can only update themselves unless they are admin
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    service = UserService(db)
    db_user = await service.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await service.update_user(user_id=user_id, user_in=user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    service = UserService(db)
    success = await service.delete_user(user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

