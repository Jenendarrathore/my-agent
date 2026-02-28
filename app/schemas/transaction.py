from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.transaction import TransactionType, TransactionSource


class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: TransactionType
    occurred_at: datetime
    category_id: Optional[int] = None
    source: TransactionSource = TransactionSource.manual
    external_id: Optional[str] = None
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    user_id: Optional[int] = None


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    occurred_at: Optional[datetime] = None
    category_id: Optional[int] = None
    source: Optional[TransactionSource] = None
    external_id: Optional[str] = None
    notes: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
