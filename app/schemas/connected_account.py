from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.connected_account import ProviderEnum


class ConnectedAccountBase(BaseModel):
    provider: ProviderEnum
    email: EmailStr
    is_active: bool = True


class ConnectedAccountCreate(ConnectedAccountBase):
    user_id: Optional[int] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expiry: Optional[datetime] = None


class ConnectedAccountUpdate(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expiry: Optional[datetime] = None
    is_active: Optional[bool] = None


class ConnectedAccountResponse(ConnectedAccountBase):
    id: int
    user_id: int
    token_expiry: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
