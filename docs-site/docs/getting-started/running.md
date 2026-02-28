---
sidebar_position: 2
sidebar_label: "Running the App"
---

# ▶️ Running the Application

## Overview

The application consists of **4 processes** that need to run simultaneously:

| Process | Command | Port | Purpose |
|---------|---------|------|---------|
| API Server | `uvicorn app.main:app --reload` | 8000 | REST API |
| Base Worker | `./venv/bin/arq app.core.worker.base_settings.WorkerSettings` | — | General background tasks (Redis DB 1) |
| Email Worker | `./venv/bin/arq app.core.worker.email_settings.WorkerSettings` | — | Email jobs (Redis DB 2) |
| Frontend | `cd frontend && npm run dev` | 5174 | React SPA |

---

## Running with Docker Compose

```bash
# Start all services (API, workers, DB, Redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Docker Compose runs the following services:
- `db` — PostgreSQL 15 (port 5432)
- `redis` — Redis 7 (port 6379)
- `api` — FastAPI server (port 8000)
- `base_worker` — Base ARQ worker
- `email_worker` — Email ARQ worker

---

## Running Locally (Development)

### API Server
```bash
# From project root, with venv activated
uvicorn app.main:app --reload
# Runs on http://localhost:8000
# Auto-reloads on code changes
```

**Alternative** (using Python directly):
```bash
python -m app.main
```

### Workers

Each worker is a separate process. They **must be running** for background jobs to execute.

```bash
# Base Worker — handles general tasks
./venv/bin/arq app.core.worker.base_settings.WorkerSettings

# Email Worker — handles email fetch, extraction, OTP sending
./venv/bin/arq app.core.worker.email_settings.WorkerSettings
```

**Alternative** (using runner scripts):
```bash
python run_base_worker.py
python run_email_worker.py
```

### Frontend
```bash
cd frontend
npm run dev
# Runs on http://localhost:5174
```

**Build for production:**
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

---

## API Documentation

When the API server is running, interactive docs are available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Workers not picking up jobs | Ensure workers are running and Redis is accessible |
| `email_pool is None` error | The API server must be running (lifespan initializes pools) |
| Database connection errors | Check `DATABASE_URL` in `.env` and PostgreSQL is running |
| Google OAuth errors | Verify `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and redirect URI |
