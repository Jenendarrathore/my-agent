from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = None


class RoleResponse(RoleBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
