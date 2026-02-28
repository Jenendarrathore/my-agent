from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class EmailConnectionBase(BaseModel):
    provider: str
    access_token: str
    refresh_token: str
    scopes: Optional[List[str]] = None
    expires_at: datetime


class EmailConnectionCreate(EmailConnectionBase):
    user_id: int


class EmailConnectionUpdate(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scopes: Optional[List[str]] = None
    expires_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None


class EmailConnectionRead(EmailConnectionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    revoked_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
