from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.db.models import ConversationStatus, MessageRole, ThreadKind
from app.schemas.common import ORMBase


class ConversationCreateRequest(BaseModel):
    workspace_id: UUID
    title: str | None = Field(default=None, max_length=200)


class ConversationRead(ORMBase):
    id: UUID
    workspace_id: UUID
    creator_id: UUID
    title: str | None
    status: ConversationStatus
    created_at: datetime


class ThreadCreateRequest(BaseModel):
    kind: ThreadKind
    parent_thread_id: UUID | None = None


class ThreadRead(ORMBase):
    id: UUID
    conversation_id: UUID
    kind: ThreadKind
    parent_thread_id: UUID | None
    created_by: UUID
    created_at: datetime


class MessageCreateRequest(BaseModel):
    role: MessageRole = MessageRole.USER
    content_json: dict
    token_count: int | None = None


class MessageRead(ORMBase):
    id: UUID
    thread_id: UUID
    role: MessageRole
    content_json: dict
    token_count: int | None
    created_by: UUID | None
    created_at: datetime


class ContextInjectionCreateRequest(BaseModel):
    from_thread_id: UUID
    from_message_id: UUID
    to_thread_id: UUID
    to_message_id: UUID | None = None
    context_block: dict


class ContextInjectionRead(ORMBase):
    id: UUID
    conversation_id: UUID
    from_thread_id: UUID
    from_message_id: UUID
    to_thread_id: UUID
    to_message_id: UUID | None
    context_block: dict
    injected_by: UUID
    created_at: datetime
