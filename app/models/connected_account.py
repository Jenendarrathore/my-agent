import enum
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, text, ForeignKey, Enum, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProviderEnum(str, enum.Enum):
    gmail = "gmail"


class ConnectedAccount(Base):
    __tablename__ = "connected_accounts"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[ProviderEnum] = mapped_column(
        Enum(ProviderEnum, name="provider_enum"), nullable=False
    )
    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    access_token: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token: Mapped[str] = mapped_column(Text, nullable=False)
    token_expiry: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="connected_accounts")

    __table_args__ = (
        UniqueConstraint("provider", "email", name="uq_connected_account_provider_email"),
    )
