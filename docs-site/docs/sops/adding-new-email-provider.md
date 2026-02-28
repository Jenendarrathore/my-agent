---
sidebar_position: 4
sidebar_label: "Adding a New Email Provider"
---

# 📋 SOP: Adding a New Email Provider

## When to Use

Use this SOP when integrating a new email service (e.g., Outlook, IMAP, Yahoo) into the email fetch system.

---

## Step 1: Create the Provider Class

Create `app/email/providers/<provider_name>.py`:

```python
from typing import List, Optional, Any, Dict
from app.email.providers.base import EmailProvider
from app.email.dto import EmailMessage
from app.email.exceptions import EmailAuthError, EmailFetchError
from datetime import datetime, timezone


class OutlookProvider(EmailProvider):
    """
    Microsoft Outlook/Graph API implementation of EmailProvider.
    """

    def __init__(self):
        self._client = None  # Provider-specific client

    async def connect(self, credentials_data: Dict[str, Any]) -> None:
        """
        Connect using provider-specific credentials.
        credentials_data should contain access_token, refresh_token, etc.
        """
        try:
            # Initialize your provider client
            # e.g., Microsoft Graph SDK, IMAP connection, etc.
            pass
        except Exception as e:
            raise EmailAuthError(f"Connection failed: {str(e)}", provider="outlook")

    async def fetch_messages(
        self, 
        cursor: Optional[str] = None, 
        limit: int = 50
    ) -> List[EmailMessage]:
        """Fetch messages and return normalized EmailMessage DTOs."""
        if not self._client:
            raise EmailAuthError("Provider not connected", provider="outlook")
        
        try:
            # Fetch from provider API
            # Map each message to EmailMessage DTO
            messages = []
            
            # Example mapping:
            # for raw_msg in raw_messages:
            #     messages.append(EmailMessage(
            #         provider="outlook",
            #         provider_message_id=raw_msg["id"],
            #         thread_id=raw_msg.get("conversationId"),
            #         from_email=raw_msg["from"]["emailAddress"]["address"],
            #         to_emails=[r["emailAddress"]["address"] for r in raw_msg["toRecipients"]],
            #         subject=raw_msg.get("subject"),
            #         received_at=parse_datetime(raw_msg["receivedDateTime"]),
            #     ))
            
            return messages
        except Exception as e:
            raise EmailFetchError(f"Fetch failed: {str(e)}", provider="outlook")

    async def fetch_message_body(self, message_id: str) -> Optional[EmailMessage]:
        """Fetch full body for a specific message."""
        if not self._client:
            raise EmailAuthError("Provider not connected", provider="outlook")
        
        try:
            # Fetch full message content
            # Return EmailMessage with body_text and body_html populated
            pass
        except Exception as e:
            raise EmailFetchError(f"Body fetch failed: {str(e)}", provider="outlook")

    async def disconnect(self) -> None:
        """Clean up connections."""
        self._client = None
```

---

## Step 2: Register with ProviderFactory

Add to `app/email/providers/factory.py`:

```python
from app.email.providers.outlook import OutlookProvider

# At module level:
ProviderFactory.register("outlook", OutlookProvider)
```

---

## Step 3: Update Provider Enum (if needed)

The `ConnectedAccount` model already supports the provider via enum. If adding a new provider not in the enum, update `app/models/connected_account.py`:

```python
class ProviderEnum(str, enum.Enum):
    gmail = "gmail"
    outlook = "outlook"
    imap = "imap"
    other = "other"
    yahoo = "yahoo"  # New provider
```

Then generate a migration:
```bash
alembic revision --autogenerate -m "Add yahoo to provider enum"
```

> **Note**: Alembic may not auto-detect enum value changes. You may need to manually edit the migration to add the new enum value.

---

## Step 4: Handle Credentials in EmailFetchJob

The `EmailFetchJob` currently maps credentials for Gmail. Add your provider's credential mapping in `app/jobs/email_fetch.py`:

```python
if provider_name == "gmail":
    creds.update({
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET
    })
elif provider_name == "outlook":
    creds.update({
        "client_id": settings.OUTLOOK_CLIENT_ID,
        "client_secret": settings.OUTLOOK_CLIENT_SECRET,
        "tenant_id": settings.OUTLOOK_TENANT_ID,
    })
```

---

## Step 5: Add OAuth Flow (if applicable)

If the provider uses OAuth2:

1. Add env vars to `app/core/config.py`
2. Create OAuth flow endpoint (similar to `app/api/v1/google_auth.py`)
3. Handle callback and token storage

---

## Step 6: Update Connected Accounts Authorize Endpoint

Update `app/api/v1/connected_accounts.py` to handle the new provider's authorization:

```python
elif account.provider == "outlook":
    # Build Microsoft OAuth2 authorization URL
    authorization_url = build_outlook_auth_url(account_id, current_user.id)
    return {"authorization_url": authorization_url}
```

---

## Key Principles

1. **All providers return `EmailMessage` DTOs** — the rest of the system is provider-agnostic
2. **Credentials are passed at runtime** — providers are stateless between sessions
3. **Always implement `disconnect()`** — clean up resources
4. **Use provider-specific exceptions** — set `provider` field for debugging
5. **The factory pattern** means no changes needed to jobs/services — they use `ProviderFactory.get_provider(name)`

---

## Files Modified Checklist

| File | Action |
|------|--------|
| `app/email/providers/<provider>.py` | **Create** — Provider implementation |
| `app/email/providers/factory.py` | **Modify** — Register provider |
| `app/email/providers/__init__.py` | **Modify** — Import (optional) |
| `app/models/connected_account.py` | **Modify** — Add enum value (if needed) |
| `app/jobs/email_fetch.py` | **Modify** — Add credential mapping |
| `app/core/config.py` | **Modify** — Add provider env vars |
| `app/api/v1/connected_accounts.py` | **Modify** — Add authorize flow |
