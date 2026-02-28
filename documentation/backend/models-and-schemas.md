# 🧱 Models, Schemas & CRUD Pattern

## Architecture Pattern

Every domain entity follows a consistent **Model → Schema → CRUD → Service → Router** pattern:

```
Router (HTTP layer)
  ↓
Service (business logic)
  ↓
CRUD (data access)
  ↓
Model (database table)   ←→   Schema (validation/serialization)
```

---

## 1. Models (`app/models/`)

SQLAlchemy 2.0 declarative models using `Mapped` type annotations.

**Common patterns**:
```python
from app.core.database import Base

class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, 
                                      unique=True, primary_key=True)
    # ... fields ...
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )
```

**Key conventions**:
- Integer auto-increment PKs
- `created_at` with both `server_default` (for raw SQL) and Python `default`
- `ForeignKey` with `ondelete` cascade policies
- Relationships use `Mapped[]` with type string references
- `UniqueConstraint` and `Index` in `__table_args__`

**All models** (9 total): `User`, `Role`, `Category`, `Transaction`, `ConnectedAccount`, `Email`, `EmailExtraction`, `Job`, `LLMTransaction`

---

## 2. Schemas (`app/schemas/`)

Pydantic v2 models for request validation and response serialization.

**Standard schema pattern** per entity:

```python
class EntityBase(BaseModel):
    """Shared fields"""
    field1: str
    field2: Optional[str] = None

class EntityCreate(EntityBase):
    """Create request — required fields + any creation-specific fields"""
    required_field: int

class EntityUpdate(BaseModel):
    """Partial update — all fields optional"""
    field1: Optional[str] = None
    field2: Optional[str] = None

class EntityRead(EntityBase):
    """Response model with DB-computed fields"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
```

**Key conventions**:
- `ConfigDict(from_attributes=True)` — enables validating from SQLAlchemy models
- `EntityCreate` extends `EntityBase` — adds FK fields
- `EntityUpdate` is independent — all fields optional for PATCH
- `EntityRead` adds `id`, timestamps, computed fields

---

## 3. CRUD (`app/crud/`)

Pure data access functions. Async. No business logic.

**Standard operations per entity**:

```python
async def create_entity(db: AsyncSession, obj_in: EntityCreate) -> Entity:
    db_obj = Entity(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_entity(db: AsyncSession, id: int) -> Optional[Entity]:
    result = await db.execute(select(Entity).where(Entity.id == id))
    return result.scalars().first()

async def get_entities(db: AsyncSession, skip: int = 0, limit: int = 100, 
                        **filters) -> List[Entity]:
    query = select(Entity)
    # Apply optional filters...
    query = query.offset(skip).limit(limit).order_by(Entity.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())

async def update_entity(db: AsyncSession, db_obj: Entity, obj_in: EntityUpdate) -> Entity:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def delete_entity(db: AsyncSession, id: int) -> bool:
    db_obj = await get_entity(db, id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
        return True
    return False
```

**Special CRUD**: `auth.py` — handles user lookups (by email/username/id), password management, refresh tokens, OTP.

---

## 4. Services (`app/services/`)

Business logic layer. Instantiated with a DB session.

**Standard service pattern**:

```python
class EntityService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_entity(self, entity_in: EntityCreate) -> EntityRead:
        db_obj = await crud.create_entity(self.db, entity_in)
        return EntityRead.model_validate(db_obj)

    async def get_entity(self, id: int) -> Optional[EntityRead]:
        db_obj = await crud.get_entity(self.db, id)
        return EntityRead.model_validate(db_obj) if db_obj else None
    
    # ... list, update, delete follow same pattern
```

**Key**: Services always return **Pydantic schemas** (not raw models), ensuring consistent serialization.

---

## 5. Adding to `__init__.py`

When creating new models/schemas/services, register them in the respective `__init__.py`:

- `app/models/__init__.py` — import and add to `__all__`
- `app/services/__init__.py` — import and add to `__all__`
