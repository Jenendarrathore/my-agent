from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)

    name: Mapped[str] = mapped_column(String, unique=False, index=True, nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    primary_email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    otp: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    otp_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    refresh_token_expiry: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )

    categories: Mapped[List["Category"]] = relationship(
        "Category", back_populates="user", cascade="all, delete-orphan"
    )
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan"
    )
    connected_accounts: Mapped[List["ConnectedAccount"]] = relationship(
        "ConnectedAccount", back_populates="user", cascade="all, delete-orphan"
    )
    email_connections: Mapped[List["EmailConnection"]] = relationship(
        "EmailConnection", back_populates="user", cascade="all, delete-orphan"
    )
    emails: Mapped[List["Email"]] = relationship(
        "Email", back_populates="user", cascade="all, delete-orphan"
    )

