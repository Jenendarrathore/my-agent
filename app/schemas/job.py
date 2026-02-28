from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    job_type: str
    status: str = "QUEUED"
    triggered_by: str
    user_id: Optional[int] = None
    input_payload: Optional[Any] = None
    output_payload: Optional[Any] = None
    error_payload: Optional[Any] = None
    retry_count: int = 0


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    status: Optional[str] = None
    output_payload: Optional[Any] = None
    error_payload: Optional[Any] = None
    retry_count: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class JobRead(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime
