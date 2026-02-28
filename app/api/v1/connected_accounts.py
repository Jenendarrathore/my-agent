from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.connected_account import ConnectedAccountCreate, ConnectedAccountUpdate, ConnectedAccountResponse
from app.services.connected_account_service import ConnectedAccountService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/connected-accounts", tags=["connected-accounts"])


@router.post("/", response_model=ConnectedAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_connected_account(
    account_in: ConnectedAccountCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    return await service.create_account(account_in=account_in, user_id=current_user.id)


@router.get("/", response_model=List[ConnectedAccountResponse])
async def read_connected_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    return await service.list_user_accounts(user_id=current_user.id)


@router.get("/{account_id}", response_model=ConnectedAccountResponse)
async def read_connected_account(
    account_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    account = await service.get_account(account_id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Connected account not found")
    return account


@router.patch("/{account_id}", response_model=ConnectedAccountResponse)
async def update_connected_account(
    account_id: int, 
    account_in: ConnectedAccountUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    account = await service.get_account(account_id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Connected account not found")
    return await service.update_account(account_id=account_id, account_in=account_in)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connected_account(
    account_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    account = await service.get_account(account_id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Connected account not found")
        
    success = await service.delete_account(account_id=account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Connected account not found")
    return None

