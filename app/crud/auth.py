from datetime import datetime, timezone, timedelta
from typing import Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.role import Role
from app.schemas.auth import UserRegister
from app.core.security import get_password_hash, verify_password


async def get_role_by_name(db: AsyncSession, name: str) -> Optional[Role]:
    result = await db.execute(select(Role).where(Role.name == name))
    return result.scalars().first()


async def get_default_role(db: AsyncSession) -> Role:
    role = await get_role_by_name(db, "user")
    if not role:
        role = Role(name="user")
        db.add(role)
        await db.commit()
        await db.refresh(role)
    return role


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.primary_email == email).options(selectinload(User.role))
    )
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.username == username).options(selectinload(User.role))
    )
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.role))
    )
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: UserRegister) -> User:
    role = await get_default_role(db)
    db_user = User(
        username=user_in.username,
        primary_email=user_in.primary_email,
        password_hash=get_password_hash(user_in.password),
        role_id=role.id,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    # Reload with role
    return await get_user_by_id(db, db_user.id)


async def authenticate_user(
    db: AsyncSession, identifier: str, password: str
) -> Optional[User]:
    # identifier can be email or username
    result = await db.execute(
        select(User)
        .where(or_(User.username == identifier, User.primary_email == identifier))
        .options(selectinload(User.role))
    )
    user = result.scalars().first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def update_refresh_token(
    db: AsyncSession, user: User, refresh_token: str, expiry: datetime
) -> None:
    # We store the raw token or hashed? Requirement says recommended hashed.
    # But for ease of refresh, we might just store hashed and verify.
    # Let's use get_password_hash/verify_password for consistency
    user.refresh_token = get_password_hash(refresh_token)
    user.refresh_token_expiry = expiry
    await db.commit()


async def verify_refresh_token(
    db: AsyncSession, user_id: int, refresh_token: str
) -> Optional[User]:
    user = await get_user_by_id(db, user_id)
    if not user or not user.refresh_token or not user.refresh_token_expiry:
        return None
    
    if datetime.now(timezone.utc) > user.refresh_token_expiry.replace(tzinfo=timezone.utc):
        return None
        
    if not verify_password(refresh_token, user.refresh_token):
        return None
        
    return user


async def update_user_password(
    db: AsyncSession, user: User, new_password: str
) -> None:
    user.password_hash = get_password_hash(new_password)
    # Also invalidate refresh sessions on password change
    user.refresh_token = None
    user.refresh_token_expiry = None
    user.otp = None
    user.otp_expires_at = None
    await db.commit()


async def save_user_otp(
    db: AsyncSession, user: User, otp: str, expires_at: datetime
) -> None:
    user.otp = otp
    user.otp_expires_at = expires_at
    await db.commit()


async def clear_user_otp(db: AsyncSession, user: User) -> None:
    user.otp = None
    user.otp_expires_at = None
    await db.commit()
