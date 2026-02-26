# FastAPI Production-Ready Boilerplate 🚀

This is a production-ready FastAPI boilerplate with async PostgreSQL, SQLAlchemy, Alembic migrations, and specialized ARQ/Redis workers.

## 🛠 Tech Stack

- **FastAPI**: Modern, high-performance web framework.
- **PostgreSQL**: Robust relational database.
- **SQLAlchemy (Async)**: Modern SQL toolkit and Async ORM.
- **Alembic**: Database migrations for SQLAlchemy.
- **ARQ**: Specialized async task queues based on Redis.
- **Redis**: Message broker and optional cache store.
- **Pydantic Settings**: Type-safe settings management.

## 📁 Project Structure

```text
.
├── app/
│   ├── main.py             # App entry point
│   ├── core/               # Infrastructure & Setup
│   │   ├── worker/         # Specialized worker settings
│   │   ├── setup.py        # Centralized app factory (lifespan, routing)
│   │   ├── queue.py        # Pool placeholders
│   │   ├── config.py       # Pydantic Settings
│   │   ├── database.py     # Async DB Engine & Session
│   │   └── redis.py        # Redis client
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic validation schemas
│   ├── routes/             # API Router definitions
│   ├── services/           # Reusable business logic
│   └── workers/            # ARQ Job functions
│       └── jobs.py
├── run_base_worker.py      # Entry script for DB 1 worker
├── run_email_worker.py     # Entry script for DB 2 worker
├── alembic/                # Database migrations
├── docker-compose.yml       # Production/Dev orchestration
├── Dockerfile              # API/Worker build definition
└── README.md
```

## 🚀 Getting Started

### 1. Clone & Environment
```bash
cp .env.example .env
```

### 2. Run with Docker Compose
```bash
docker-compose up --build
```
- **API**: [http://localhost:8000](http://localhost:8000)
- **Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Database Migrations
Always run migrations after model changes:
```bash
# Generate
docker-compose exec api alembic revision --autogenerate -m "Add table X"
# Apply
docker-compose exec api alembic upgrade head
```

## 🌐 API Endpoints

- `GET /`: Health check.
- `POST /users`: Create user & trigger background job.
- `GET /users`: List users.
- `GET /users/{id}`: Get user details.

## 🏗 Developing Locally (Native)

### 1. Prerequisites
- **Python 3.11+**
- **PostgreSQL**: Create `fastapi_db`.
- **Redis**: Running on `6379`.

### 2. Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start Services
Run these in separate terminal windows:

- **API:**
  ```bash
  uvicorn app.main:app --reload
  ```
- **Base Worker:**
  ```bash
  arq app.core.worker.base_settings.WorkerSettings
  ```
- **Email Worker:**
  ```bash
  arq app.core.worker.email_settings.WorkerSettings
  ```

---
*For detailed architecture notes and guides on adding new queues, see [setup.md](setup.md).*
