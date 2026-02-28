import enum
from datetime import datetime, timezone

from sqlalchemy import String, Boolean, DateTime, text, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CategoryType(str, enum.Enum):
    income = "income"
    expense = "expense"
    both = "both"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[CategoryType] = mapped_column(
        Enum(CategoryType, name="category_type"), default=CategoryType.expense
    )
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_category_user_name"),
    )
