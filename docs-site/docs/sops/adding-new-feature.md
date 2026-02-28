---
sidebar_position: 1
sidebar_label: "Adding a New Feature"
---

# 📋 SOP: Adding a New Feature

## Overview

This SOP covers the end-to-end process of adding a new feature to the application — from model creation through to frontend integration.

---

## Step-by-Step Checklist

### 1. Define the Data Model

- [ ] Create model file: `app/models/<entity>.py`
- [ ] Follow the standard pattern (see [Models & Schemas](../backend/models-and-schemas.md))
- [ ] Register in `app/models/__init__.py`

```python
# app/models/my_entity.py
from app.core.database import Base
from sqlalchemy import String, DateTime, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

class MyEntity(Base):
    __tablename__ = "my_entities"
    
    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )
```

### 2. Create Pydantic Schemas

- [ ] Create schema file: `app/schemas/<entity>.py`
- [ ] Define `Base`, `Create`, `Update`, `Read` schemas

```python
# app/schemas/my_entity.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MyEntityBase(BaseModel):
    name: str

class MyEntityCreate(MyEntityBase):
    user_id: int

class MyEntityUpdate(BaseModel):
    name: Optional[str] = None

class MyEntityRead(MyEntityBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    created_at: datetime
```

### 3. Create CRUD Functions

- [ ] Create CRUD file: `app/crud/<entity>.py`
- [ ] Implement `create`, `get`, `get_all`, `update`, `delete`

### 4. Create Service

- [ ] Create service file: `app/services/<entity>_service.py`
- [ ] Register in `app/services/__init__.py`

### 5. Generate Migration

```bash
alembic revision --autogenerate -m "Add my_entity table"
alembic upgrade head
```

### 6. Create API Router

- [ ] Create router file: `app/api/v1/<entities>.py`
- [ ] Register in `app/api/v1/__init__.py`

```python
# app/api/v1/__init__.py
from .my_entities import router as my_entities_router
router.include_router(my_entities_router)
```

### 7. Test the API

```bash
# Use interactive docs
open http://localhost:8000/docs
```

### 8. Frontend (Optional)

- [ ] Create page: `frontend/src/pages/MyEntities.tsx`
- [ ] Add route in `App.tsx`
- [ ] Add nav item in `MainLayout.tsx`

---

## File Checklist Summary

| Layer | File to Create/Modify |
|-------|-----------------------|
| Model | `app/models/<entity>.py` + `app/models/__init__.py` |
| Schema | `app/schemas/<entity>.py` |
| CRUD | `app/crud/<entity>.py` |
| Service | `app/services/<entity>_service.py` + `app/services/__init__.py` |
| Migration | `alembic revision --autogenerate` |
| Router | `app/api/v1/<entities>.py` + `app/api/v1/__init__.py` |
| Frontend | `frontend/src/pages/<Entity>.tsx` + `App.tsx` + `MainLayout.tsx` |
