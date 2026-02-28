from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class EmailBase(BaseModel):
    provider: str
    provider_message_id: str
    thread_id: Optional[str] = None
    subject: Optional[str] = None
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    received_at: datetime
    checksum: Optional[str] = None
    extraction_status: str = "PENDING"
    extraction_version: Optional[str] = None


class EmailCreate(EmailBase):
    user_id: int
    email_connection_id: int


class EmailUpdate(BaseModel):
    extraction_status: Optional[str] = None
    extraction_version: Optional[str] = None


class EmailRead(EmailBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    email_connection_id: int
    fetched_at: datetime
    created_at: datetime
