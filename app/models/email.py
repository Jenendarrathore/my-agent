from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, DateTime, text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    connected_account_id: Mapped[int] = mapped_column(ForeignKey("connected_accounts.id"), nullable=False)
    
    provider: Mapped[str] = mapped_column(String, nullable=False)
    provider_message_id: Mapped[str] = mapped_column(String, nullable=False)
    thread_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    subject: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    body_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    body_html: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    checksum: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )
    
    extraction_status: Mapped[str] = mapped_column(String, default="PENDING", nullable=False)
    extraction_version: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        UniqueConstraint("provider", "provider_message_id", name="uq_email_provider_message_id"),
    )

    user: Mapped["User"] = relationship("User", back_populates="emails")
    connected_account: Mapped["ConnectedAccount"] = relationship("ConnectedAccount", back_populates="emails")
    extractions: Mapped[List["EmailExtraction"]] = relationship("EmailExtraction", back_populates="email", cascade="all, delete-orphan")
