from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.dependencies.auth import get_current_user
from app.models.user import User


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_in: TransactionCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    return await service.create_transaction(transaction_in=transaction_in, user_id=current_user.id)


@router.get("/", response_model=List[TransactionResponse])
async def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    return await service.list_user_transactions(user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def read_transaction(
    transaction_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    transaction = await service.get_transaction(transaction_id=transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int, 
    transaction_in: TransactionUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    transaction = await service.get_transaction(transaction_id=transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return await service.update_transaction(transaction_id=transaction_id, transaction_in=transaction_in)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    transaction = await service.get_transaction(transaction_id=transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    success = await service.delete_transaction(transaction_id=transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return None

