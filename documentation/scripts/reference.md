# 🛠️ Scripts Reference

## Overview

All scripts are located in `app/scripts/`. They are standalone utilities for testing, setup, and maintenance.

---

## Running Scripts

All scripts should be run from the **project root** with the virtual environment activated:

```bash
source venv/bin/activate
python -m app.scripts.<script_name>
# or
python app/scripts/<script_name>.py
```

---

## Available Scripts

### `cleanup_db.py`
**Purpose**: Database cleanup utility — removes test data or resets database state.

**Usage**:
```bash
python app/scripts/cleanup_db.py
```

---

### `setup_user_gmail.py`
**Purpose**: Sets up a Gmail connection for a user. Creates a `ConnectedAccount` record with the user's Gmail address.

**Usage**:
```bash
python app/scripts/setup_user_gmail.py
```

---

### `test_api_crud.py`
**Purpose**: Integration test script that exercises all API CRUD endpoints — creates, reads, updates, and deletes records across all entities via HTTP calls.

**Usage**:
```bash
python app/scripts/test_api_crud.py
```

**Prerequisite**: API server must be running.

---

### `test_email_abstraction.py`
**Purpose**: Tests the email provider abstraction layer — verifies `EmailProvider` interface, `ProviderFactory`, and DTO mapping.

**Usage**:
```bash
python app/scripts/test_email_abstraction.py
```

---

### `test_gmail_structure.py`
**Purpose**: Tests Gmail API response structure — verifies the format of message metadata and body responses.

**Usage**:
```bash
python app/scripts/test_gmail_structure.py
```

**Prerequisite**: Valid Google OAuth tokens configured.

---

### `test_job_system.py`
**Purpose**: Tests the background job system — verifies `BaseJob`, `JobRunner`, `EmailFetchJob`, and `EmailExtractionJob` execution, lifecycle hooks, and DB record management.

**Usage**:
```bash
python app/scripts/test_job_system.py
```

**Prerequisite**: Database and Redis must be accessible.

---

### `test_roles_crud.py`
**Purpose**: Tests Role CRUD operations — creates roles, assigns to users, verifies role-based queries.

**Usage**:
```bash
python app/scripts/test_roles_crud.py
```

---

## Other Utilities

### `migrate.sh`
**Location**: Project root

**Purpose**: Quick migration shortcut — generates and applies a migration in one step.

```bash
# Usage:
bash migrate.sh

# Contents:
# alembic revision --autogenerate -m "Add table X"
# alembic upgrade head
```

> **Note**: Edit the message before running.

### `run_base_worker.py`
**Location**: Project root

**Purpose**: Alternative way to start the base worker.

```bash
python run_base_worker.py
```

### `run_email_worker.py`
**Location**: Project root

**Purpose**: Alternative way to start the email worker.

```bash
python run_email_worker.py
```
