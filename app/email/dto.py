from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EmailMessage(BaseModel):
    """Normalized Data Transfer Object for email messages."""
    provider: str
    provider_message_id: str
    thread_id: Optional[str] = None
    from_email: str
    to_emails: List[str]
    subject: Optional[str] = None
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    received_at: datetime
    checksum: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
