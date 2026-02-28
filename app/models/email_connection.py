from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, DateTime, text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class EmailConnection(Base):
    __tablename__ = "email_connections"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    provider: Mapped[str] = mapped_column(String, index=True, nullable=False)
    access_token: Mapped[str] = mapped_column(String, nullable=False)  # encrypted placeholder string
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)  # encrypted placeholder string
    scopes: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
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

    user: Mapped["User"] = relationship("User", back_populates="email_connections")
    emails: Mapped[List["Email"]] = relationship("Email", back_populates="email_connection", cascade="all, delete-orphan")
