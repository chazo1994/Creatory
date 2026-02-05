from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.db.models import SourceType
from app.schemas.common import ORMBase


class KnowledgeSourceCreateRequest(BaseModel):
    workspace_id: UUID
    source_type: SourceType
    uri: str | None = None
    title: str | None = None
    metadata_json: dict = Field(default_factory=dict)


class KnowledgeSourceRead(ORMBase):
    id: UUID
    workspace_id: UUID
    source_type: SourceType
    uri: str | None
    title: str | None
    metadata_json: dict
    ingest_status: str
    created_by: UUID
    created_at: datetime


class KnowledgeChunkCreateRequest(BaseModel):
    content: str = Field(min_length=1)
    token_count: int | None = None
    metadata_json: dict = Field(default_factory=dict)


class KnowledgeChunkRead(ORMBase):
    id: UUID
    source_id: UUID
    chunk_index: int
    content: str
    token_count: int | None
    metadata_json: dict
