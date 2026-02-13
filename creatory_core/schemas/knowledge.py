from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from creatory_core.db.models import SourceType
from creatory_core.schemas.common import ORMBase


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


class KnowledgeQueryRequest(BaseModel):
    workspace_id: UUID
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class KnowledgeCitation(BaseModel):
    index: int
    chunk_id: UUID
    source_id: UUID
    source_title: str | None = None
    score: float
    content: str


class KnowledgeQueryResponse(BaseModel):
    query: str
    answer_preview: str
    citations: list[KnowledgeCitation]
