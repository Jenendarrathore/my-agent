from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    primary_email: EmailStr


class UserCreate(UserBase):
    password: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    primary_email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
