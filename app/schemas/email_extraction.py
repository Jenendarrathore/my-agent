from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class EmailExtractionBase(BaseModel):
    extraction_version: Optional[str] = None
    status: str
    extracted_json: Optional[Any] = None
    model_used: Optional[str] = None
    prompt_hash: Optional[str] = None


class EmailExtractionCreate(EmailExtractionBase):
    email_id: int


class EmailExtractionRead(EmailExtractionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email_id: int
    created_at: datetime
