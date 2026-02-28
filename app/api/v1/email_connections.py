from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.email_connection import EmailConnectionCreate, EmailConnectionUpdate, EmailConnectionRead
from app.services.email_connection_service import EmailConnectionService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/email-connections", tags=["email-connections"])


@router.post("/", response_model=EmailConnectionRead, status_code=status.HTTP_201_CREATED)
async def create_connection(
    connection_in: EmailConnectionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailConnectionService(db)
    # Ensure user_id matches current_user
    if connection_in.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create connection for another user")
    return await service.create_connection(connection_in)


@router.get("/", response_model=List[EmailConnectionRead])
async def read_connections(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailConnectionService(db)
    return await service.list_user_connections(user_id=current_user.id)


@router.get("/{connection_id}", response_model=EmailConnectionRead)
async def read_connection(
    connection_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailConnectionService(db)
    connection = await service.get_connection(connection_id)
    if not connection or connection.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Email connection not found")
    return connection


@router.patch("/{connection_id}", response_model=EmailConnectionRead)
async def update_connection(
    connection_id: int,
    connection_in: EmailConnectionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailConnectionService(db)
    connection = await service.get_connection(connection_id)
    if not connection or connection.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Email connection not found")
    return await service.update_connection(connection_id, connection_in)


@router.delete("/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connection(
    connection_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailConnectionService(db)
    connection = await service.get_connection(connection_id)
    if not connection or connection.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Email connection not found")
    
    success = await service.delete_connection(connection_id)
    if not success:
        raise HTTPException(status_code=404, detail="Email connection not found")
    return None
