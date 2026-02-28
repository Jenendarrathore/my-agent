# Developer Guide 👨‍💻

This guide provides everything a developer needs to know to set up, develop, and maintain this application.

## ⚙️ Environment Setup

### 1. Local Python Environment
We recommend using Python 3.11+.

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Infrastructure Requirements
The app requires **PostgreSQL** (Port 5432) and **Redis** (Port 6379).

**Recommended**: Use Docker Compose to spin up only the databases if you want to run the API natively:
```bash
docker-compose up -d db redis
```

### 3. Environment Variables
Copy `.env.example` to `.env` and fill in your credentials.
- `DATABASE_URL`: `postgresql+asyncpg://user:pass@localhost:5432/fastapi_db`
- `REDIS_URL`: `redis://localhost:6379`
- `SECRET_KEY`: Use a secure random string.

---

## 🛠 Working with the Database

### Creating Migrations
When you change a model in `app/models/`, you must generate a migration:
```bash
./venv/bin/alembic revision --autogenerate -m "Description of changes"
```

### Applying Migrations
```bash
./venv/bin/alembic upgrade head
```

### Resetting the Database
To wipe the database and re-apply all migrations:
```bash
dropdb fastapi_db
createdb fastapi_db
./venv/bin/alembic upgrade head
```

---

## 🏃‍♂️ Running the Application

### Starting the API
```bash
uvicorn app.main:app --reload
```
API will be available at [http://localhost:8000](http://localhost:8000).

### Starting Background Workers
Each worker runs in its own process. You need both for full functionality:
- **Base Worker**: `arq app.core.worker.base_settings.WorkerSettings`
- **Email Worker**: `arq app.core.worker.email_settings.WorkerSettings`

Alternatively, use the provided scripts:
```bash
python run_base_worker.py
python run_email_worker.py
```

---

## 🏗 Development Workflow

### Adding a New Model
1. Create a new file in `app/models/`.
2. Inherit from `Base`.
3. Import the new model in `app/models/__init__.py`.
4. Run `alembic revision --autogenerate`.

### Adding a New API Endpoint
1. Define Pydantic schemas in `app/schemas/`.
2. Implement CRUD logic in `app/crud/`.
3. Implement Service orchestration in `app/services/`.
4. Create/update routes in `app/api/v1/`.
5. Ensure the router is included in `app/api/__init__.py` or `app/main.py`.

### Protecting a Route
Inject the `get_current_user` dependency:
```python
from app.dependencies.auth import get_current_user
from app.models.user import User

@router.get("/my-data")
async def get_my_data(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id}
```

---

## 📖 Key Documentation
- **[features.md](features.md)**: High-level overview of what the app does.
- **[auth.md](auth.md)**: Deep dive into the Authentication & OTP implementation.
- **[setup.md](setup.md)**: Details on the multi-queue architecture and lifespan management.
- **[TESTING.md](TESTING.md)**: Comprehensive guide for API CRUD verification testing.
