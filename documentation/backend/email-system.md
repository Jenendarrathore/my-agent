# ✉️ Email System

## Overview

The email system uses a **provider abstraction pattern** to support multiple email services (Gmail, Outlook, IMAP, etc.) through a unified interface.

---

## Architecture

```
┌──────────────────────────────────────────┐
│            Email System                   │
│                                          │
│  ┌─────────────────────────────────────┐ │
│  │ EmailProvider (Abstract Base Class)  │ │
│  │  ├─ connect(credentials)            │ │
│  │  ├─ fetch_messages(cursor, limit)   │ │
│  │  ├─ fetch_message_body(message_id)  │ │
│  │  └─ disconnect()                    │ │
│  └────────────┬────────────────────────┘ │
│               │ implements                │
│  ┌────────────▼────────────────────────┐ │
│  │ GmailProvider                        │ │
│  │  Uses Google Gmail API + OAuth2      │ │
│  │  Token refresh built-in              │ │
│  └──────────────────────────────────────┘ │
│                                          │
│  ┌──────────────────────────────────────┐ │
│  │ ProviderFactory (Registry Pattern)   │ │
│  │  .register(name, cls)               │ │
│  │  .get_provider(name) → instance     │ │
│  └──────────────────────────────────────┘ │
│                                          │
│  ┌──────────────────────────────────────┐ │
│  │ EmailMessage (DTO)                   │ │
│  │  Normalized data transfer object     │ │
│  └──────────────────────────────────────┘ │
│                                          │
│  ┌──────────────────────────────────────┐ │
│  │ Exceptions                           │ │
│  │  EmailProviderError (base)           │ │
│  │  ├─ EmailAuthError                   │ │
│  │  ├─ EmailFetchError                  │ │
│  │  └─ EmailRateLimitError              │ │
│  └──────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

---

## Components

### EmailProvider (Base Class) — `app/email/providers/base.py`

Abstract interface that all email providers must implement:

```python
class EmailProvider(ABC):
    async def connect(self, credentials: Any) -> None: ...
    async def fetch_messages(self, cursor=None, limit=50) -> List[EmailMessage]: ...
    async def fetch_message_body(self, message_id: str) -> Optional[EmailMessage]: ...
    async def disconnect(self) -> None: ...
```

### EmailMessage (DTO) — `app/email/dto.py`

Normalized data transfer object returned by all providers:

```python
class EmailMessage(BaseModel):
    provider: str              # "gmail", "outlook", etc.
    provider_message_id: str   # Provider's unique message ID
    thread_id: Optional[str]
    from_email: str
    to_emails: List[str]
    subject: Optional[str]
    body_text: Optional[str]
    body_html: Optional[str]
    received_at: datetime
    checksum: Optional[str]
```

### ProviderFactory — `app/email/providers/factory.py`

Registry pattern for provider discovery:

```python
ProviderFactory.register("gmail", GmailProvider)
# Usage:
provider = ProviderFactory.get_provider("gmail")  # Returns GmailProvider()
```

---

## GmailProvider — `app/email/providers/gmail.py`

### Connection
- Uses `google.oauth2.credentials.Credentials` with OAuth2 tokens
- Auto-refreshes expired tokens via `credentials.refresh(Request())`
- Builds Gmail API service: `build("gmail", "v1", credentials=...)`

### Fetching Messages
1. Calls `users().messages().list(userId='me', maxResults=limit)` for message IDs
2. For each message, fetches metadata via `users().messages().get(format='metadata')`
3. Maps response to `EmailMessage` DTO

### Fetching Message Body
- Calls `users().messages().get(format='full')` for a specific message
- Recursively walks MIME parts to extract `text/plain` and `text/html` bodies
- Handles base64url encoding

### Credential Requirements
```python
{
    "access_token": "...",
    "refresh_token": "...",
    "client_id": settings.GOOGLE_CLIENT_ID,
    "client_secret": settings.GOOGLE_CLIENT_SECRET
}
```

---

## Exception Hierarchy

```
EmailProviderError (base)
├── EmailAuthError       — OAuth/connection failures
├── EmailFetchError      — Message fetch failures
└── EmailRateLimitError  — Rate limiting (future use)
```

All exceptions carry a `provider` field for debugging.

---

## OTP Email Delivery

OTP emails for password reset are sent via ARQ:

1. `forgot_password` route generates OTP, stores in DB
2. Enqueues `send_otp_email` job via `queue.email_pool`
3. Email worker picks up job
4. Currently prints to console (mock implementation):

```python
async def send_otp_email(ctx, email: str, otp: str):
    print(f"To: {email}")
    print(f"OTP: {otp}")
    print(f"Valid for 5 minutes.")
```

> **Note**: Replace with actual SMTP/SendGrid/SES in production.

---

## Email Processing Pipeline

```
1. User connects Gmail account (OAuth2)
2. User triggers fetch → POST /api/v1/jobs/trigger/fetch
3. Email Worker executes EmailFetchJob:
   - Connects to Gmail with stored tokens
   - Fetches messages
   - Deduplicates by (provider, provider_message_id)
   - Stores in emails table (status: PENDING)
4. User triggers extraction → POST /api/v1/jobs/trigger/extract
5. Email Worker executes EmailExtractionJob:
   - Selects PENDING emails
   - Processes via LLM (mock/real)
   - Creates EmailExtraction records
   - Creates Transaction records from extracted data
   - Updates email status to COMPLETED/FAILED
```
