from app.email.providers import ProviderFactory
from app.services.email_service import EmailService
from app.services.connected_account_service import ConnectedAccountService
from app.schemas.email import EmailCreate
from app.jobs.base import BaseJob
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class EmailFetchJob(BaseJob):
    """
    Job to fetch emails from a provider and store them in the database.
    """

    async def run(self) -> Dict[str, Any]:
        user_id = self.input_payload.get("user_id")
        provider_name = self.input_payload.get("provider", "gmail")
        limit = self.input_payload.get("limit", 20)
        cursor = self.input_payload.get("cursor")
        account_id = self.input_payload.get("account_id")

        if not user_id:
            raise ValueError("user_id is required in input_payload")

        # 1. Get credentials for user
        conn_service = ConnectedAccountService(self.db)
        
        if account_id:
            account = await conn_service.get_account_db(account_id)
            if not account or account.user_id != user_id:
                raise ValueError(f"Account {account_id} not found or doesn't belong to user {user_id}")
            provider_name = account.provider.value
        else:
            # Fallback to legacy logic: find first active account for provider
            accounts = await conn_service.list_user_accounts_db(user_id)
            account = next((a for a in accounts if a.provider == provider_name and a.is_active), None)
        
        if not account:
            raise ValueError(f"No active {provider_name} account found")

        # 2. Get Provider from Factory
        try:
            provider = ProviderFactory.get_provider(provider_name)
        except ValueError as e:
            logger.error(f"Error getting provider: {str(e)}")
            raise

        try:
            # 3. Connect (using tokens from DB)
            from app.core.config import settings
            # Mapping credentials dynamically based on provider could be handled in factory or here
            creds = {
                "access_token": account.access_token,
                "refresh_token": account.refresh_token,
            }
            
            # Add provider specific settings if needed
            if provider_name == "gmail":
                creds.update({
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET
                })
            
            await provider.connect(creds)

            # 4. Fetch
            messages = await provider.fetch_messages(cursor=cursor, limit=limit)
            logger.info(f"Fetched {len(messages)} messages for user {user_id}")

            # 5. Store & Deduplicate
            email_service = EmailService(self.db)
            saved_count = 0
            
            for msg in messages:
                # Check if exists
                existing = await email_service.get_email_by_provider_id(
                    user_id=user_id, 
                    provider=msg.provider, 
                    provider_message_id=msg.provider_message_id
                )
                if not existing:
                    email_in = EmailCreate(
                        user_id=user_id,
                        connected_account_id=account.id,
                        provider=msg.provider,
                        provider_message_id=msg.provider_message_id,
                        thread_id=msg.thread_id,
                        subject=msg.subject,
                        received_at=msg.received_at
                    )
                    await email_service.create_email(email_in)
                    saved_count += 1

            await self.db.commit()
            
            return {
                "fetched_count": len(messages),
                "saved_count": saved_count,
                "user_id": user_id
            }

        finally:
            # Always disconnect
            await provider.disconnect()
