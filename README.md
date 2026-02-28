# FastAPI Production-Ready Boilerplate 🚀

This is a production-ready FastAPI boilerplate with async PostgreSQL, SQLAlchemy, Alembic migrations, and specialized ARQ/Redis workers.

## 📖 Essential Documentation
- **[DEVELOPMENT.md](DEVELOPMENT.md)**: 🛠 **Start here** for local setup, database management, and development workflow.
- **[features.md](features.md)**: 🌟 Full list of implemented features (Auth, Finance CRUD, Infrastructure).
- **[auth.md](auth.md)**: 🔒 Detailed breakdown of the Secure Auth & OTP implementation.
- **[TESTING.md](TESTING.md)**: 🧪 **API Verification**: Detailed guide on running the full CRUD test suite.
- **[setup.md](setup.md)**: 🏗 Multi-worker architecture and queue expansion guide.

## 🚀 Quick Start (Docker)
If you have Docker installed, you can get the entire stack running in seconds:

```bash
cp .env.example .env
docker-compose up --build
```

- **API**: [http://localhost:8000](http://localhost:8000)
- **Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📁 Core Project Structure
```text
.
├── app/
│   ├── main.py             # App entry point
│   ├── core/               # Infrastructure & Setup
│   ├── models/             # SQLAlchemy modern models
│   ├── schemas/            # Pydantic V2 validation
│   ├── api/                # API Routes (Auth, v1)
│   ├── services/           # Business logic & Orchestration
│   ├── crud/               # Database operations
│   └── workers/            # ARQ background jobs
├── alembic/                # Database migrations
├── docker-compose.yml       # Production/Dev orchestration
└── requirements.txt        # Pinned dependencies
```
