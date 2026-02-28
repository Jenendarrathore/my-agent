from datetime import datetime, timezone
from typing import Optional, Any
from sqlalchemy import String, DateTime, text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class EmailExtraction(Base):
    __tablename__ = "email_extractions"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    email_id: Mapped[int] = mapped_column(ForeignKey("emails.id"), nullable=False)
    
    extraction_version: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)  # SUCCESS, FAILED
    extracted_json: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    
    model_used: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    prompt_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )

    email: Mapped["Email"] = relationship("Email", back_populates="extractions")
