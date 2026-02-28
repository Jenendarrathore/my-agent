# 📋 SOP: Adding a New Database Model

## When to Use

Use this SOP when you need to add a new database entity (table) to the application.

---

## Step 1: Create the Model

Create `app/models/<entity>.py`:

```python
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, DateTime, text, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class NewEntity(Base):
    __tablename__ = "new_entities"

    # Primary Key (always)
    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    
    # Foreign Key (if applicable)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    
    # Fields
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamp (always)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="new_entities")
```

### Conventions
- **Table name**: lowercase, plural, snake_case
- **PK**: Always `id`, integer, autoincrement
- **FK**: Use `ondelete` policy (`CASCADE`, `SET NULL`, `RESTRICT`)
- **Timestamps**: `created_at` with both `server_default` and Python `default`
- **Optional fields**: Use `Mapped[Optional[str]]` + `nullable=True`
- **Indexes**: Add `index=True` on commonly queried columns

---

## Step 2: Register the Model

Add to `app/models/__init__.py`:

```python
from app.models.new_entity import NewEntity

__all__ = [
    # ... existing models
    "NewEntity",
]
```

> **Important**: This ensures Alembic auto-discovers the model.

---

## Step 3: Add Back-Reference (if FK exists)

If your model references `User`, add the back-reference in `app/models/user.py`:

```python
new_entities: Mapped[List["NewEntity"]] = relationship(
    "NewEntity", back_populates="user", cascade="all, delete-orphan"
)
```

---

## Step 4: Generate and Apply Migration

```bash
# Generate
alembic revision --autogenerate -m "Add new_entity table"

# Review the generated file in alembic/versions/
# Then apply
alembic upgrade head
```

---

## Step 5: Create Schema, CRUD, Service, Router

Follow the [Adding a New Feature](adding-new-feature.md) SOP for the remaining layers.

---

## Special Cases

### Enums
```python
import enum

class StatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"

status: Mapped[StatusEnum] = mapped_column(
    Enum(StatusEnum, name="status_enum"), nullable=False
)
```

### Unique Constraints
```python
__table_args__ = (
    UniqueConstraint("user_id", "name", name="uq_entity_user_name"),
)
```

### Composite Indexes
```python
__table_args__ = (
    Index("idx_entity_user_date", "user_id", "created_at"),
)
```

### JSON Fields
```python
from sqlalchemy import JSON
metadata: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
```
