import asyncio
import argparse
from datetime import datetime, timedelta, timezone
from app.core.database import AsyncSessionLocal
from app.services.user_service import UserService
from app.services.connected_account_service import ConnectedAccountService
from app.schemas.user import UserCreate
from app.schemas.connected_account import ConnectedAccountCreate, ProviderEnum

async def setup(real_tokens: bool = False):
    access_token = "mock_access_token"
    refresh_token = "mock_refresh_token"

    if real_tokens:
        print("\n🔑 Real Gmail Token Setup")
        access_token = input("Enter Access Token: ").strip()
        refresh_token = input("Enter Refresh Token: ").strip()

    async with AsyncSessionLocal() as db:
        user_service = UserService(db)
        account_service = ConnectedAccountService(db)

        # 1. Create User
        ts = int(datetime.now().timestamp())
        user = await user_service.create_user(UserCreate(
            name="Gmail Tester",
            username=f"tester_{ts}",
            primary_email=f"tester_{ts}@gmail.com",
            password="Password123!"
        ))
        
        # 2. Link Gmail
        await account_service.create_account(ConnectedAccountCreate(
            provider=ProviderEnum.gmail,
            email=user.primary_email,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expiry=datetime.now(timezone.utc) + timedelta(hours=1)
        ), user_id=user.id)
        
        await db.commit()
        print(f"✅ Setup complete for User: {user.username} (ID: {user.id})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--real", action="store_true", help="Ask for real OAuth tokens")
    args = parser.parse_args()
    
    asyncio.run(setup(real_tokens=args.real))
