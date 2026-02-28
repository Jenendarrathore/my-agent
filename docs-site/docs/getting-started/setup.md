---
sidebar_position: 1
sidebar_label: "Setup Guide"
---

# 🛠️ Setup Guide

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 18+ | Frontend build tooling |
| PostgreSQL | 15+ | Primary database |
| Redis | 7+ | Caching, OTP, job queues |
| Docker & Docker Compose | Latest | (Optional) Container orchestration |

---

## Option A: Docker Setup (Recommended for Quick Start)

```bash
# 1. Clone the repository
git clone <repository-url>
cd my-agent

# 2. Copy environment variables
cp .env.example .env
# Edit .env if needed (defaults work with Docker Compose)

# 3. Start all services
docker-compose up -d

# 4. Run migrations
docker-compose exec api alembic upgrade head

# 5. Access the app
# API:      http://localhost:8000
# API Docs: http://localhost:8000/docs
# Frontend: http://localhost:5174
```

---

## Option B: Local Development Setup

### 1. Install Dependencies

```bash
# Backend
cd my-agent
python -m venv venv
source venv/bin/activate          # Linux/macOS
# .\venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

```bash
# Frontend
cd frontend
npm install
```

### 2. Set Up PostgreSQL

```bash
# Create database (if not using Docker)
createdb fastapi_db
# Or via psql:
# CREATE DATABASE fastapi_db;
```

### 3. Set Up Redis

```bash
# Start Redis (if not using Docker)
redis-server
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your local values:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-key-change-it
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```

### 5. Run Database Migrations

```bash
# Apply all migrations
alembic upgrade head
```

### 6. Start the Application

You need **4 terminal windows**:

```bash
# Terminal 1: API Server
uvicorn app.main:app --reload

# Terminal 2: Base Worker (Redis DB 1)
./venv/bin/arq app.core.worker.base_settings.WorkerSettings

# Terminal 3: Email Worker (Redis DB 2)
./venv/bin/arq app.core.worker.email_settings.WorkerSettings

# Terminal 4: Frontend
cd frontend && npm run dev
```

---

## Google OAuth2 Setup (for Gmail Integration)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select an existing one
3. Enable the **Gmail API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Set **Authorized redirect URIs** to: `http://localhost:8000/api/v1/auth/google/callback`
6. Copy the Client ID and Client Secret to your `.env` file

---

## Verify Setup

```bash
# Health check
curl http://localhost:8000/
# Expected: {"status": "ok"}

# API docs
open http://localhost:8000/docs

# Frontend
open http://localhost:5174
```
