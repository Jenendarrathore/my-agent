from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.llm_transaction import LLMTransactionCreate, LLMTransactionRead
from app.services.llm_transaction_service import LLMTransactionService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/llm-transactions", tags=["llm-transactions"])


@router.post("/", response_model=LLMTransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_in: LLMTransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = LLMTransactionService(db)
    return await service.create_transaction(transaction_in)


@router.get("/job/{job_id}", response_model=List[LLMTransactionRead])
async def read_job_transactions(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = LLMTransactionService(db)
    return await service.list_job_transactions(job_id=job_id)


@router.get("/{transaction_id}", response_model=LLMTransactionRead)
async def read_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = LLMTransactionService(db)
    transaction = await service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = LLMTransactionService(db)
    transaction = await service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    success = await service.delete_transaction(transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return None
