from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.db.models import AssetType
from app.schemas.common import ORMBase


class MediaAssetCreateRequest(BaseModel):
    workspace_id: UUID
    type: AssetType
    storage_uri: str = Field(min_length=1)
    source_message_id: UUID | None = None
    source_tool_invocation_id: UUID | None = None
    metadata_json: dict = Field(default_factory=dict)


class MediaAssetRead(ORMBase):
    id: UUID
    workspace_id: UUID
    owner_id: UUID
    type: AssetType
    storage_uri: str
    source_message_id: UUID | None
    source_tool_invocation_id: UUID | None
    metadata_json: dict
    created_at: datetime
