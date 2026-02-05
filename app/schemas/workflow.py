from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.db.models import NodeType, RunStatus
from app.schemas.common import ORMBase


class WorkflowNodePayload(BaseModel):
    node_key: str = Field(min_length=1, max_length=120)
    type: NodeType
    config_json: dict = Field(default_factory=dict)
    position_x: float | None = None
    position_y: float | None = None


class WorkflowEdgePayload(BaseModel):
    source_node_key: str = Field(min_length=1, max_length=120)
    target_node_key: str = Field(min_length=1, max_length=120)
    condition_expr: str | None = None
    metadata_json: dict = Field(default_factory=dict)


class WorkflowTemplateCreateRequest(BaseModel):
    workspace_id: UUID
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    version: int = Field(default=1, ge=1)
    is_public: bool = False
    definition_json: dict = Field(default_factory=dict)
    nodes: list[WorkflowNodePayload] = Field(default_factory=list)
    edges: list[WorkflowEdgePayload] = Field(default_factory=list)


class WorkflowTemplateRead(ORMBase):
    id: UUID
    workspace_id: UUID
    name: str
    description: str | None
    version: int
    is_public: bool
    definition_json: dict
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class WorkflowNodeRead(ORMBase):
    id: UUID
    template_id: UUID
    node_key: str
    type: NodeType
    config_json: dict
    position_x: float | None
    position_y: float | None


class WorkflowEdgeRead(ORMBase):
    id: UUID
    template_id: UUID
    source_node_key: str
    target_node_key: str
    condition_expr: str | None
    metadata_json: dict


class WorkflowTemplateDetail(WorkflowTemplateRead):
    nodes: list[WorkflowNodeRead] = Field(default_factory=list)
    edges: list[WorkflowEdgeRead] = Field(default_factory=list)


class WorkflowRunCreateRequest(BaseModel):
    conversation_id: UUID | None = None
    input_json: dict = Field(default_factory=dict)


class WorkflowRunRead(ORMBase):
    id: UUID
    template_id: UUID
    conversation_id: UUID | None
    status: RunStatus
    input_json: dict
    output_json: dict
    started_at: datetime | None
    ended_at: datetime | None
    created_by: UUID
    created_at: datetime


class WorkflowRunStepRead(ORMBase):
    id: UUID
    workflow_run_id: UUID
    node_key: str
    status: RunStatus
    attempt: int
    input_json: dict
    output_json: dict
    error_json: dict | None
    started_at: datetime | None
    ended_at: datetime | None
    created_at: datetime


class WorkflowRunDetail(WorkflowRunRead):
    steps: list[WorkflowRunStepRead] = Field(default_factory=list)
