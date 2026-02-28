from datetime import datetime, timezone
from typing import Optional, Any, List
from sqlalchemy import String, DateTime, text, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    
    job_type: Mapped[str] = mapped_column(String, nullable=False)  # EMAIL_FETCH, EMAIL_EXTRACTION, EMAIL_REPROCESS
    status: Mapped[str] = mapped_column(String, default="QUEUED", nullable=False)  # QUEUED, RUNNING, SUCCESS, FAILED, CANCELLED
    triggered_by: Mapped[str] = mapped_column(String, nullable=False)  # CRON, MANUAL, API, RETRY
    
    input_payload: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    output_payload: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    error_payload: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        default=lambda: datetime.now(timezone.utc)
    )

    llm_transactions: Mapped[List["LLMTransaction"]] = relationship("LLMTransaction", back_populates="job", cascade="all, delete-orphan")
