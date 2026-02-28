from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.email import EmailCreate, EmailUpdate, EmailRead
from app.services.email_service import EmailService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/emails", tags=["emails"])


@router.post("/", response_model=EmailRead, status_code=status.HTTP_201_CREATED)
async def create_email(
    email_in: EmailCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailService(db)
    if email_in.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create email for another user")
    return await service.create_email(email_in)


@router.get("/", response_model=List[EmailRead])
async def read_emails(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailService(db)
    return await service.list_user_emails(user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{email_id}", response_model=EmailRead)
async def read_email(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailService(db)
    email = await service.get_email(email_id)
    if not email or email.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


@router.patch("/{email_id}", response_model=EmailRead)
async def update_email(
    email_id: int,
    email_in: EmailUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailService(db)
    email = await service.get_email(email_id)
    if not email or email.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Email not found")
    return await service.update_email(email_id, email_in)


@router.delete("/{email_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_email(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailService(db)
    email = await service.get_email(email_id)
    if not email or email.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Email not found")
    
    success = await service.delete_email(email_id)
    if not success:
        raise HTTPException(status_code=404, detail="Email not found")
    return None
