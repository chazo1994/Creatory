from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMBase


class WorkspaceCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    slug: str | None = Field(default=None, max_length=120)


class WorkspaceRead(ORMBase):
    id: UUID
    name: str
    slug: str
    owner_id: UUID
    created_at: datetime


class WorkspaceMembershipRead(BaseModel):
    workspace_id: UUID
    user_id: UUID
    role: str
    created_at: datetime
