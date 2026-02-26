from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.redis import get_redis
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user, get_user, list_users
from app.core import queue

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_redis),  # Ensure Redis is initialized
):
    # Create user in DB
    user = await create_user(db, user_in)
    # Enqueue background email job specifically to the email pool
    if queue.email_pool:
        await queue.email_pool.enqueue_job("send_email", user_id=user.id)
    return user

@router.get("/{user_id}", response_model=UserRead)
async def get_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_user(db, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("", response_model=list[UserRead])
async def list_users_endpoint(db: AsyncSession = Depends(get_db)):
    return await list_users(db)
