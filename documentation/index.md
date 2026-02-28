# 📚 Financial Agent — System Documentation

> **Comprehensive documentation for the Financial Agent application** — a full-stack FinTech platform built with FastAPI, SQLAlchemy, ARQ, and React.

---

## 🗺️ Navigation

### 🏗️ Architecture
| Document | Description |
|----------|-------------|
| [System Overview](architecture/overview.md) | Tech stack, high-level architecture diagram, and design decisions |
| [Data Flow & Request Lifecycle](architecture/data-flow.md) | How a request is made, processed, and returned |
| [Database Schema](architecture/database-schema.md) | All models, relationships, indexes, and constraints |

---

### 🚀 Getting Started
| Document | Description |
|----------|-------------|
| [Setup Guide](getting-started/setup.md) | Prerequisites, installation, and environment configuration |
| [Running the Application](getting-started/running.md) | How to run the API server, workers, and frontend |
| [Environment Variables](getting-started/environment-variables.md) | Complete `.env` configuration reference |

---

### ⚙️ Backend Deep-Dive
| Document | Description |
|----------|-------------|
| [Project Structure](backend/project-structure.md) | Directory layout and file organization |
| [Authentication System](backend/authentication.md) | Login, JWT, OAuth2, OTP, password reset |
| [API Reference](backend/api-reference.md) | All endpoints, request/response formats |
| [Models & Schemas](backend/models-and-schemas.md) | SQLAlchemy models, Pydantic schemas, CRUD layer |
| [Service Layer](backend/services.md) | Business logic services and their responsibilities |
| [Jobs & Workers](backend/jobs-and-workers.md) | ARQ setup, queues, job lifecycle, creating jobs |
| [Email System](backend/email-system.md) | Provider abstraction, Gmail integration, email fetch |
| [Database Migrations](backend/migrations.md) | Alembic setup, creating and running migrations |

---

### 🎨 Frontend
| Document | Description |
|----------|-------------|
| [Frontend Overview](frontend/overview.md) | React app architecture, pages, routing, and auth flow |

---

### 📋 Standard Operating Procedures (SOPs)
| Document | Description |
|----------|-------------|
| [Adding a New Feature](sops/adding-new-feature.md) | End-to-end SOP for building new functionality |
| [Adding a New Model](sops/adding-new-model.md) | SOP for new database models and domain entities |
| [Adding a New Background Job](sops/adding-new-job.md) | SOP for creating and registering new ARQ jobs |
| [Adding a New Worker](sops/adding-new-worker.md) | SOP for creating, configuring, and running new isolated queue workers |
| [Adding a New Email Provider](sops/adding-new-email-provider.md) | SOP for integrating new email providers (Outlook, IMAP, etc.) |

---

### 🛠️ Scripts & Utilities
| Document | Description |
|----------|-------------|
| [Scripts Reference](scripts/reference.md) | All available scripts, what they do, and how to run them |

---

## Quick Reference

```bash
# Start everything locally
uvicorn app.main:app --reload                                    # API Server
./venv/bin/arq app.core.worker.base_settings.WorkerSettings      # Base Worker
./venv/bin/arq app.core.worker.email_settings.WorkerSettings     # Email Worker
cd frontend && npm run dev                                       # Frontend

# Database Migrations
alembic revision --autogenerate -m "description"                 # Generate
alembic upgrade head                                             # Apply
```
