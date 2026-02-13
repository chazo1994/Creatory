from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from creatory_core.schemas.agent import AgentRunRead, TaskRead
from creatory_core.schemas.conversation import MessageRead


class ChatRunRequest(BaseModel):
    prompt: str = Field(min_length=1)
    assistant_agent_slug: str | None = Field(default=None, max_length=120)
    metadata_json: dict = Field(default_factory=dict)


class ChatRunResponse(BaseModel):
    user_message: MessageRead
    assistant_message: MessageRead
    agent_run: AgentRunRead
    tasks: list[TaskRead]


class RunProgressEvent(BaseModel):
    run_id: UUID
    status: str
    timestamp: datetime
    payload: dict = Field(default_factory=dict)
