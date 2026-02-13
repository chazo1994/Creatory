from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from creatory_core.db.models import RunStatus
from creatory_core.schemas.common import ORMBase


class AgentCreateRequest(BaseModel):
    workspace_id: UUID | None = None
    slug: str = Field(min_length=1, max_length=120)
    display_name: str = Field(min_length=1, max_length=120)
    persona_prompt: str = Field(min_length=1)
    config_json: dict = Field(default_factory=dict)
    is_system: bool = False


class AgentRead(ORMBase):
    id: UUID
    workspace_id: UUID | None
    slug: str
    display_name: str
    persona_prompt: str
    config_json: dict
    is_system: bool
    created_at: datetime


class AgentRunRead(ORMBase):
    id: UUID
    conversation_id: UUID | None
    thread_id: UUID | None
    agent_id: UUID
    status: RunStatus
    input_json: dict
    output_json: dict
    error_json: dict | None
    started_at: datetime | None
    ended_at: datetime | None
    created_at: datetime


class TaskRead(ORMBase):
    id: UUID
    agent_run_id: UUID
    parent_task_id: UUID | None
    task_type: str
    status: RunStatus
    input_json: dict
    output_json: dict
    error_json: dict | None
    started_at: datetime | None
    ended_at: datetime | None
    created_at: datetime
