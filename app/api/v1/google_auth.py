import json
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from google_auth_oauthlib.flow import Flow

from app.core.database import get_db
from app.core.config import settings
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.connected_account_service import ConnectedAccountService
from app.schemas.connected_account import ConnectedAccountCreate, ProviderEnum

router = APIRouter(prefix="/auth/google", tags=["google-auth"])

# Google scopes required for fetching emails
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.readonly"
]

def get_google_flow() -> Flow:
    return Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )

@router.get("/callback")
async def callback(
    code: str, 
    state: str, 
    db: AsyncSession = Depends(get_db)
):
    """
    Step 2: Handle Google redirect, exchange code for tokens, and save.
    """
    flow = get_google_flow()
    
    try:
        # Parse state
        try:
            state_data = json.loads(state)
            account_id = state_data.get("account_id")
            user_id = state_data.get("user_id")
        except:
            raise HTTPException(status_code=400, detail="Invalid state parameter")

        if not account_id:
            raise HTTPException(status_code=400, detail="Missing account_id in state")

        # Exchange authorization code for tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Verify email matches the account's email (security check)
        from googleapiclient.discovery import build
        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        google_email = user_info.get('email')
        
        conn_service = ConnectedAccountService(db)
        account = await conn_service.get_account(account_id)
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        if google_email != account.email:
            raise HTTPException(
                status_code=400, 
                detail=f"Email mismatch. Expected {account.email}, but got {google_email}"
            )

        # Update the account with tokens
        from app.schemas.connected_account import ConnectedAccountUpdate
        update_data = ConnectedAccountUpdate(
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_expiry=credentials.expiry.replace(tzinfo=timezone.utc),
            is_active=True
        )
        await conn_service.update_account(account_id, update_data)
        await db.commit()
        
        # Redirect back to frontend
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard?status=success&provider=gmail")

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=f"OAuth2 callback failed: {str(e)}")

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=f"OAuth2 callback failed: {str(e)}")
