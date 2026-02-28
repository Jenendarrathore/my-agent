import enum
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, text, ForeignKey, Enum, UniqueConstraint, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class ProviderEnum(str, enum.Enum):
    gmail = "gmail"
    outlook = "outlook"
    imap = "imap"
    other = "other"


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
    access_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    scopes: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    token_expiry: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="connected_accounts")
    emails: Mapped[List["Email"]] = relationship("Email", back_populates="connected_account", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("provider", "email", name="uq_connected_account_provider_email"),
    )
