from datetime import datetime, timezone, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.crud.auth import (
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user_by_username,
    update_refresh_token,
    verify_refresh_token,
)
from app.schemas.auth import UserRegister, UserLogin, LoginResponse, Token, UserResponse, ForgotPasswordRequest, ResetPasswordRequest
from app.core.otp import generate_otp
from app.core import queue
from app.crud.auth import save_user_otp, clear_user_otp, update_user_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)
) -> Any:
    user = await get_user_by_email(db, email=request.email)
    if not user:
        return {"message": "If an account exists with this email, an OTP has been sent."}
    
    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    await save_user_otp(db, user, otp, expires_at)
    
    if queue.email_pool:
        await queue.email_pool.enqueue_job("send_otp_email", request.email, otp)
    
    return {"message": "If an account exists with this email, an OTP has been sent."}


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)
) -> Any:
    user = await get_user_by_email(db, email=request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user.otp or user.otp != request.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP",
        )
    
    if not user.otp_expires_at or datetime.now(timezone.utc) > user.otp_expires_at.replace(tzinfo=timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expired OTP",
        )
    
    await update_user_password(db, user, request.new_password)
    
    return {"message": "Password updated successfully"}


@router.post("/register", response_model=Token)
async def register(
    user_in: UserRegister, db: AsyncSession = Depends(get_db)
) -> Any:
    user = await get_user_by_email(db, email=user_in.primary_email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    user = await get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists.",
        )
    
    user = await create_user(db, user_in=user_in)
    
    access_token = create_access_token(user.id, user.role.name)
    refresh_token = create_refresh_token(user.id)
    
    # Update refresh token in DB
    expiry = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    await update_refresh_token(db, user, refresh_token, expiry)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Any:
    user = await authenticate_user(
        db, identifier=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    
    access_token = create_access_token(user.id, user.role.name)
    refresh_token = create_refresh_token(user.id)
    
    # Update refresh token in DB
    expiry = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    await update_refresh_token(db, user, refresh_token, expiry)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user,
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str, db: AsyncSession = Depends(get_db)
) -> Any:
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
        
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user = await verify_refresh_token(db, user_id, refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    
    access_token = create_access_token(user.id, user.role.name)
    # Optionally rotate refresh token here as well
    # For now, just return new access token with same refresh token
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
