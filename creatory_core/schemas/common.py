from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserPublic(ORMBase):
    id: UUID
    email: str
    display_name: str | None = None
    avatar_url: str | None = None
    created_at: datetime
