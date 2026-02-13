from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from creatory_core.db.models import RunStatus, TransportType
from creatory_core.schemas.common import ORMBase


class MCPServerCreateRequest(BaseModel):
    workspace_id: UUID
    name: str = Field(min_length=1, max_length=120)
    transport: TransportType
    endpoint: str | None = None
    auth_config_json: dict = Field(default_factory=dict)
    is_active: bool = True


class MCPServerRead(ORMBase):
    id: UUID
    workspace_id: UUID
    name: str
    transport: TransportType
    endpoint: str | None
    auth_config_json: dict
    is_active: bool
    created_at: datetime


class MCPToolCreateRequest(BaseModel):
    tool_name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    input_schema: dict
    output_schema: dict | None = None
    capabilities_json: dict = Field(default_factory=dict)


class MCPToolRead(ORMBase):
    id: UUID
    mcp_server_id: UUID
    tool_name: str
    description: str | None
    input_schema: dict
    output_schema: dict | None
    capabilities_json: dict
    created_at: datetime


class ToolInvocationRead(ORMBase):
    id: UUID
    task_id: UUID | None
    workflow_run_step_id: UUID | None
    mcp_tool_id: UUID
    request_json: dict
    response_json: dict
    status: RunStatus
    error_code: str | None
    latency_ms: int | None
    started_at: datetime | None
    ended_at: datetime | None
    created_at: datetime
