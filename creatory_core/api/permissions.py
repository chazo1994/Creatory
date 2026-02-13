import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.db.models import Conversation, Thread, WorkspaceMembership


async def ensure_workspace_member(
    db: AsyncSession,
    workspace_id: uuid.UUID,
    user_id: uuid.UUID,
) -> WorkspaceMembership:
    membership = await db.scalar(
        select(WorkspaceMembership).where(
            WorkspaceMembership.workspace_id == workspace_id,
            WorkspaceMembership.user_id == user_id,
        )
    )
    if membership is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    return membership


async def ensure_conversation_member(
    db: AsyncSession,
    conversation_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Conversation:
    conversation = await db.get(Conversation, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    await ensure_workspace_member(db, conversation.workspace_id, user_id)
    return conversation


async def ensure_thread_in_conversation(
    db: AsyncSession,
    thread_id: uuid.UUID,
    conversation_id: uuid.UUID,
) -> Thread:
    thread = await db.get(Thread, thread_id)
    if thread is None or thread.conversation_id != conversation_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")
    return thread
