from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.email_extraction import EmailExtractionCreate, EmailExtractionRead
from app.services.email_extraction_service import EmailExtractionService
from app.services.email_service import EmailService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/email-extractions", tags=["email-extractions"])


@router.post("/", response_model=EmailExtractionRead, status_code=status.HTTP_201_CREATED)
async def create_extraction(
    extraction_in: EmailExtractionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify email belongs to user
    email_service = EmailService(db)
    email = await email_service.get_email(extraction_in.email_id)
    if not email or email.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Email not found")
        
    service = EmailExtractionService(db)
    return await service.create_extraction(extraction_in)


@router.get("/email/{email_id}", response_model=List[EmailExtractionRead])
async def read_email_extractions(
    email_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify email belongs to user
    email_service = EmailService(db)
    email = await email_service.get_email(email_id)
    if not email or email.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Email not found")
        
    service = EmailExtractionService(db)
    return await service.list_email_extractions(email_id=email_id)


@router.get("/{extraction_id}", response_model=EmailExtractionRead)
async def read_extraction(
    extraction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailExtractionService(db)
    extraction = await service.get_extraction(extraction_id)
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
        
    # Verify email belongs to user
    email_service = EmailService(db)
    email = await email_service.get_email(extraction.email_id)
    if not email or email.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Extraction not found")
        
    return extraction


@router.delete("/{extraction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_extraction(
    extraction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = EmailExtractionService(db)
    extraction = await service.get_extraction(extraction_id)
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
        
    # Verify email belongs to user
    email_service = EmailService(db)
    email = await email_service.get_email(extraction.email_id)
    if not email or email.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Extraction not found")
    
    success = await service.delete_extraction(extraction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Extraction not found")
    return None
