from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class LLMTransactionBase(BaseModel):
    model_name: str
    provider: str
    prompt_version: Optional[str] = None
    prompt_hash: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    latency_ms: int = 0


class LLMTransactionCreate(LLMTransactionBase):
    job_id: Optional[int] = None


class LLMTransactionRead(LLMTransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: Optional[int] = None
    created_at: datetime
