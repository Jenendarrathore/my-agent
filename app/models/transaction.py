import enum
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, text, ForeignKey, Enum, Numeric, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"


class TransactionSource(str, enum.Enum):
    manual = "manual"
    gmail = "gmail"
    import_source = "import"  # "import" is a reserved word
    api = "api"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        "category_id", ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type"), nullable=False
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, nullable=False
    )
    source: Mapped[TransactionSource] = mapped_column(
        Enum(TransactionSource, name="transaction_source"), default=TransactionSource.manual
    )
    external_id: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    category: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="transactions"
    )

    __table_args__ = (
        Index("idx_transactions_user_occurred_at", "user_id", "occurred_at"),
    )
