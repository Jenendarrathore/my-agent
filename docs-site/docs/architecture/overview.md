---
sidebar_position: 1
sidebar_label: "System Overview"
---

# 🏗️ System Architecture Overview

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Framework** | FastAPI | Async REST API with auto-generated OpenAPI docs |
| **Language** | Python 3.11+ | Backend language |
| **ORM** | SQLAlchemy 2.0 (async) | Database models and queries |
| **Database** | PostgreSQL 15 | Primary relational database |
| **Migrations** | Alembic | Database schema versioning |
| **Cache / Queues** | Redis 7 | OTP storage, ARQ job queues |
| **Task Queue** | ARQ | Async background job processing |
| **Auth** | JWT (python-jose) + bcrypt (passlib) | Token-based authentication |
| **Email Provider** | Google Gmail API | OAuth2-based email fetching |
| **LLM** | OpenAI (mock) | Financial data extraction from emails |
| **Frontend** | React 18 + TypeScript + Vite | Single-page application |
| **CSS** | TailwindCSS 3 | Utility-first styling |
| **Containerization** | Docker + Docker Compose | Multi-service orchestration |

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        CLIENT (React SPA)                           │
│  Vite + React 18 + TypeScript + TailwindCSS + React Router          │
│  Pages: Login, Register, Dashboard, Emails, Jobs, ConnectedAccounts │
└──────────────┬───────────────────────────────────────────────────────┘
               │ HTTP (axios)
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     FastAPI APPLICATION                              │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                    API Layer (Routers)                        │    │
│  │  /api/auth/*        → Auth (register, login, refresh, OTP)   │    │
│  │  /api/v1/users/*    → User CRUD                              │    │
│  │  /api/v1/roles/*    → Role CRUD                              │    │
│  │  /api/v1/emails/*   → Email CRUD                             │    │
│  │  /api/v1/jobs/*     → Job CRUD + Trigger endpoints           │    │
│  │  /api/v1/categories/*          → Category CRUD               │    │
│  │  /api/v1/transactions/*        → Transaction CRUD            │    │
│  │  /api/v1/connected-accounts/*  → OAuth accounts              │    │
│  │  /api/v1/email-extractions/*   → Extraction results          │    │
│  │  /api/v1/llm-transactions/*    → LLM usage logs              │    │
│  │  /api/v1/auth/google/*         → Google OAuth2 flow          │    │
│  └──────────────┬───────────────────────────────────────────────┘    │
│                 │                                                    │
│  ┌──────────────▼───────────────────────────────────────────────┐    │
│  │              Service Layer (Business Logic)                   │    │
│  │  UserService, EmailService, JobService, TaskService,          │    │
│  │  TransactionService, CategoryService, ConnectedAccountService,│    │
│  │  EmailExtractionService, LLMTransactionService,               │    │
│  │  RoleService, MockLLMService                                  │    │
│  └──────────────┬───────────────────────────────────────────────┘    │
│                 │                                                    │
│  ┌──────────────▼───────────────────────────────────────────────┐    │
│  │                CRUD Layer (Data Access)                        │    │
│  │  auth, user, role, email, job, transaction, category,         │    │
│  │  connected_account, email_extraction, llm_transaction         │    │
│  └──────────────┬───────────────────────────────────────────────┘    │
│                 │                                                    │
└─────────────────┼────────────────────────────────────────────────────┘
                  │
    ┌─────────────▼──────────────┐     ┌───────────────────────────────┐
    │      PostgreSQL 15         │     │          Redis 7              │
    │  ─────────────────────     │     │  ────────────────────         │
    │  users, roles, emails,     │     │  DB 0 → OTP / cache          │
    │  jobs, transactions,       │     │  DB 1 → Base worker queue    │
    │  categories, connected_    │     │  DB 2 → Email worker queue   │
    │  accounts, email_          │     │                               │
    │  extractions,              │     │                               │
    │  llm_transactions          │     │                               │
    └────────────────────────────┘     └──────────────┬────────────────┘
                                                      │
                                       ┌──────────────▼────────────────┐
                                       │     ARQ Workers               │
                                       │  ──────────────────           │
                                       │  Base Worker (DB 1)           │
                                       │   └─ sample_task              │
                                       │                               │
                                       │  Email Worker (DB 2)          │
                                       │   ├─ send_email               │
                                       │   ├─ send_otp_email           │
                                       │   ├─ run_email_fetch          │
                                       │   └─ run_email_extraction     │
                                       └───────────────────────────────┘
```

---

## Key Design Decisions

### 1. Layered Architecture
The backend follows a strict **Router → Service → CRUD → Model** layering:
- **Routers** handle HTTP concerns (validation, status codes, auth guards)
- **Services** contain business logic and orchestration
- **CRUD** handles raw database operations
- **Models** define the database schema

### 2. Multi-Queue Worker Architecture
ARQ workers use **logical Redis database isolation** (not separate Redis instances):
- **DB 1** — Base queue for general tasks
- **DB 2** — Email queue for email-specific tasks

This allows independent scaling of workers by type.

### 3. Application Factory Pattern
The `create_application()` function in `app/core/setup.py` centralizes app creation. It:
- Configures lifespan (Redis + ARQ pool init/teardown)
- Sets up CORS middleware
- Includes all routers

### 4. Provider Abstraction for Email
Email providers implement an abstract `EmailProvider` base class. New providers (Outlook, IMAP) can be added via the `ProviderFactory` without touching existing code.

### 5. Job System Abstraction
All background jobs extend `BaseJob` and are orchestrated by `JobRunner`, which handles:
- Job record creation
- Lifecycle hooks (`before_run`, `run`, `after_run`, `on_failure`)
- Status tracking and error recording
