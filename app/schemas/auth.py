from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None


class UserBase(BaseModel):
    username: str
    primary_email: EmailStr


class UserRegister(UserBase):
    password: str


class UserLogin(BaseModel):
    identifier: str  # email or username
    password: str


class RoleSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: RoleSchema
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
