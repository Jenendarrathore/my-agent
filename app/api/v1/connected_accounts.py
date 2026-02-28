from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.connected_account import ConnectedAccountCreate, ConnectedAccountUpdate, ConnectedAccountResponse
from app.services.connected_account_service import ConnectedAccountService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/connected-accounts", tags=["connected-accounts"])


@router.post("/", response_model=ConnectedAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_connected_account(
    account_in: ConnectedAccountCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    return await service.create_account(account_in=account_in, user_id=current_user.id)


@router.get("/", response_model=List[ConnectedAccountResponse])
async def read_connected_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    return await service.list_user_accounts(user_id=current_user.id)


@router.get("/{account_id}", response_model=ConnectedAccountResponse)
async def read_connected_account(
    account_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    account = await service.get_account(account_id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Connected account not found")
    return account


@router.patch("/{account_id}", response_model=ConnectedAccountResponse)
async def update_connected_account(
    account_id: int, 
    account_in: ConnectedAccountUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    account = await service.get_account(account_id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Connected account not found")
    return await service.update_account(account_id=account_id, account_in=account_in)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connected_account(
    account_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ConnectedAccountService(db)
    account = await service.get_account(account_id=account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Connected account not found")
        
    success = await service.delete_account(account_id=account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Connected account not found")
    return None


@router.get("/{account_id}/authorize")
async def authorize_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Unified endpoint to initiate authorization for any provider.
    """
    service = ConnectedAccountService(db)
    account = await service.get_account(account_id=account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Connected account not found")

    if account.provider == "gmail":
        # Call Google-specific logic
        from app.api.v1.google_auth import get_google_flow
        import json
        
        flow = get_google_flow()
        state_data = json.dumps({"account_id": account_id, "user_id": current_user.id})
        
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
            state=state_data,
            login_hint=account.email
        )
        return {"authorization_url": authorization_url}
    
    elif account.provider in ["outlook", "imap", "other"]:
        # Future-proofing: Return a friendly error or 'Coming Soon' logic
        raise HTTPException(
            status_code=501, 
            detail=f"Authorization for {account.provider} is not yet implemented."
        )
    
    raise HTTPException(status_code=400, detail="Unsupported provider")


@router.post("/{account_id}/fetch", status_code=status.HTTP_202_ACCEPTED)
async def trigger_account_fetch(
    account_id: int,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Trigger an immediate email fetch job for a specific account.
    """
    from app.services.task_service import TaskService
    
    service = ConnectedAccountService(db)
    account = await service.get_account(account_id=account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Connected account not found")

    await TaskService.enqueue_email_fetch(
        user_id=current_user.id,
        provider=account.provider.value,
        limit=limit,
        account_id=account.id
    )
    
    return {"message": f"Fetch job enqueued for {account.email}", "account_id": account_id}

