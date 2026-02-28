---
sidebar_position: 8
sidebar_label: "Migrations"
---

# 🔄 Database Migrations (Alembic)

## Overview

The project uses **Alembic** with async PostgreSQL (asyncpg) for database migrations. Migrations are auto-generated from SQLAlchemy model changes.

---

## Setup

### Configuration Files

| File | Purpose |
|------|---------|
| `alembic.ini` | Alembic main config (script location, logging) |
| `alembic/env.py` | Migration environment — loads models, overrides DB URL |
| `alembic/script.py.mako` | Template for new migration files |
| `alembic/versions/` | Generated migration files |

### How Alembic Was Set Up

1. **Installed**: `pip install alembic`
2. **Initialized**: `alembic init alembic`
3. **Configured `alembic.ini`**:
   ```ini
   script_location = alembic
   prepend_sys_path = .
   sqlalchemy.url = postgresql+asyncpg://postgres:postgres@db:5432/fastapi_db
   ```
4. **Modified `alembic/env.py`**:
   - Uses `async_engine_from_config` for async support
   - Imports `Base` from `app.models.user`
   - **Auto-discovers all models** via `import_models("app.models")` (walks package recursively)
   - Overrides `sqlalchemy.url` with `settings.DATABASE_URL` from environment

### Key `env.py` Snippet

```python
from app.models.user import Base
from app.core.config import settings

def import_models(package_name):
    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        importlib.import_module(module_name)

import_models("app.models")
target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
```

This key design ensures **all models are registered** on Alembic's metadata before generating migrations — new models are automatically picked up.

---

## Common Commands

### Generate a New Migration

```bash
alembic revision --autogenerate -m "Add new_table"
```

This compares your SQLAlchemy models against the current DB state and generates a migration file.

### Apply All Pending Migrations

```bash
alembic upgrade head
```

### Rollback Last Migration

```bash
alembic downgrade -1
```

### View Current Migration State

```bash
alembic current
```

### View Migration History

```bash
alembic history
```

### Quick Script

A convenience script is provided:

```bash
# migrate.sh
alembic revision --autogenerate -m "Add table X"
alembic upgrade head
```

---

## Migration History

| File | Description |
|------|-------------|
| `8dfa102f486c_initial_migration.py` | Initial tables creation |
| `18145c22048e_added_auth_related_models.py` | Auth/roles models |
| `ded1b14398dd_name_added_to_user_model.py` | Name field on User |
| `0ac2ec6c313d_modfied_user_model.py` | User model changes |
| `324713d6732f_added_otp_columns_to_user_model.py` | OTP fields (otp, otp_expires_at) |
| `d0ee78d7dc0d_categories_connect_accounts_.py` | Categories + connected accounts |
| `9257d9f8cc12_add_email_and_job_models.py` | Email + Job + related models |
| `dfca4bea8251_consolidate_connected_accounts_and_.py` | Connected accounts consolidation |
| `65c81b7d03ba_add_user_id_to_jobs.py` | user_id FK on jobs table |

---

## SOP: Creating a New Migration

1. **Modify/create** your SQLAlchemy model in `app/models/`
2. **Import** the model in `app/models/__init__.py` (ensures auto-discovery)
3. **Generate** the migration:
   ```bash
   alembic revision --autogenerate -m "Descriptive message"
   ```
4. **Review** the generated file in `alembic/versions/`
5. **Apply**:
   ```bash
   alembic upgrade head
   ```

> **Important**: Always review auto-generated migrations. Alembic may miss certain changes (e.g., enum value additions, server defaults).
