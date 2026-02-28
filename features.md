# Project Features Documentation

This document summarizes all the features currently implemented in the application.

## 1. Authentication & Security
- **Secure Registration**: Create an account with username, email, and password.
- **Flexible Login**: Authenticate using either **username** or **email**.
- **Role-Based Access Control (RBAC)**:
    - Persistent `Role` system.
    - Automatic assignment of default "user" role.
- **JWT Session Management**:
    - Short-lived Access Tokens (60 minutes).
    - Long-lived, hashed Refresh Tokens (7 days) stored in the database.
    - `GET /api/v1/users/me` endpoint to retrieve current session context.
- **OTP-Based Forgot Password**:
    - Numeric 6-digit OTP generation.
    - Database-backed OTP storage with 5-minute expiration logic.
    - Secure password reset flow that invalidates existing sessions.
- **Swagger Authorization**: Built-in support for the "Authorize" button in `/docs` using `OAuth2PasswordRequestForm`.

## 2. User Management (`/api/v1/users`)
- **Profile Management**: Users can view their own profiles and list all users (depending on permissions).
- **Self-Service Updates**: Users can update their basic information (like display name).
- **Account Deletion**: Users can delete their accounts (self-only protection).
- **Privacy Protections**: Routes are protected ensuring that users can generally only modify their own data.

## 3. Financial Management (v1 Routes)
### Categories (`/api/v1/categories`)
- Full CRUD for transaction categories.
- User-specific isolation (you only see and manage your own categories).

### Transactions (`/api/v1/transactions`)
- Full CRUD for tracking financial transactions.
- Automatic link to user context via dependency injection.
- Filtering by date and amount (in CRUD logic).

### Connected Accounts (`/api/v1/connected-accounts`)
- **Unified Connection Model**: Centralized management of all external accounts (Email, Bank, etc.).
- **Multi-Account Support**: Users can link multiple accounts per provider.
- **Multi-Provider Framework**: Built-in support for **Gmail**, with architecture ready for **Outlook**, **IMAP**, and others.

## 4. Email & Job Management
- **Provider Framework**:
    - **`ProviderFactory`**: Dynamically selects the correct email provider (Gmail, Outlook, etc.) at runtime.
    - **Stateless Adapters**: Pluggable provider logic that handles OAuth2 or direct credentials.
- **Email Pipeline**:
    - Automatic background fetching and deduplication of `Emails`.
    - **Content Extraction**: Structured data parsing (e.g., invoices, transactions) with versioned extraction logic.
- **Background Jobs**:
    - Centralized `Job` tracking system (EMAIL_FETCH, EXTRACTION, etc.).
    - Status monitoring (QUEUED, RUNNING, SUCCESS, FAILED).
    - Automatic retry logic and error payload logging.
- **LLM Usage Tracking**:
    - Detailed `LLMTransaction` logs for cost and token monitoring.
    - Transaction linking to specific background jobs.

## 5. Infrastructure & Workers
- **Asynchronous Data Layer**: Powered by SQLAlchemy 2.0 with `asyncpg` for non-blocking database operations.
- **Automated Migrations**: Full integration with Alembic for safe schema evolution.
- **Specialized Task Queues (ARQ & Redis)**:
    - **Base Queue**: For general database-heavy background tasks.
    - **Email Queue**: Dedicated queue for notification and OTP delivery.
- **Logical Database Isolation**: Workers use separate Redis logical databases for task isolation.
- **Containerization**: Fully Dockerized setup with `docker-compose` for easy deployment.

## 6. Documentation
- **[auth.md](auth.md)**: Deep dive into the security implementation.
- **[walkthrough.md](file:///home/jenendar/.gemini/antigravity/brain/b93a104f-9822-41d3-8566-014f18434138/walkthrough.md)**: Implementation history and verification results.
- **Swagger Docs**: Interactive API playground at `/docs`.
