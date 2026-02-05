import asyncio
import json
import uuid
from datetime import UTC, datetime
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.api.permissions import ensure_conversation_member, ensure_thread_in_conversation
from app.db.models import AgentRun, Task, User
from app.db.session import get_db_session
from app.schemas.agent import AgentRunRead, TaskRead
from app.schemas.conversation import MessageRead
from app.schemas.orchestrator import ChatRunRequest, ChatRunResponse
from app.services.director import run_director_turn

router = APIRouter(prefix="/orchestration", tags=["orchestration"])


@router.post(
    "/conversations/{conversation_id}/threads/{thread_id}/chat",
    response_model=ChatRunResponse,
    status_code=status.HTTP_201_CREATED,
)
async def run_chat_turn(
    conversation_id: uuid.UUID,
    thread_id: uuid.UUID,
    payload: ChatRunRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ChatRunResponse:
    conversation = await ensure_conversation_member(db, conversation_id, current_user.id)
    thread = await ensure_thread_in_conversation(db, thread_id, conversation.id)

    result = await run_director_turn(
        db=db,
        current_user=current_user,
        conversation=conversation,
        thread=thread,
        payload=payload,
    )

    return ChatRunResponse(
        user_message=MessageRead.model_validate(result.user_message),
        assistant_message=MessageRead.model_validate(result.assistant_message),
        agent_run=AgentRunRead.model_validate(result.agent_run),
        tasks=[TaskRead.model_validate(task) for task in result.tasks],
    )


@router.get("/runs/{run_id}", response_model=AgentRunRead)
async def get_run(
    run_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> AgentRunRead:
    run = await db.get(AgentRun, run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    if run.conversation_id is not None:
        await ensure_conversation_member(db, run.conversation_id, current_user.id)

    return AgentRunRead.model_validate(run)


@router.get("/runs/{run_id}/tasks", response_model=list[TaskRead])
async def list_run_tasks(
    run_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[TaskRead]:
    run = await db.get(AgentRun, run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    if run.conversation_id is not None:
        await ensure_conversation_member(db, run.conversation_id, current_user.id)

    tasks = (
        await db.scalars(
            select(Task).where(Task.agent_run_id == run.id).order_by(Task.created_at.asc())
        )
    ).all()
    return [TaskRead.model_validate(task) for task in tasks]


@router.get("/runs/{run_id}/stream")
async def stream_run(
    run_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> StreamingResponse:
    run = await db.get(AgentRun, run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    if run.conversation_id is not None:
        await ensure_conversation_member(db, run.conversation_id, current_user.id)

    tasks = (
        await db.scalars(
            select(Task).where(Task.agent_run_id == run.id).order_by(Task.created_at.asc())
        )
    ).all()

    async def event_stream() -> AsyncGenerator[str, None]:
        start_payload = {
            "run_id": str(run.id),
            "status": run.status.value,
            "at": datetime.now(UTC).isoformat(),
            "stage": "start",
        }
        yield (
            "event: run\n"
            f"data: {json.dumps(start_payload)}\n\n"
        )
        await asyncio.sleep(0)

        for task in tasks:
            payload = {
                "run_id": str(run.id),
                "task_id": str(task.id),
                "task_type": task.task_type,
                "status": task.status.value,
                "at": datetime.now(UTC).isoformat(),
            }
            yield f"event: task\ndata: {json.dumps(payload)}\n\n"
            await asyncio.sleep(0)

        final_payload = {
            "run_id": str(run.id),
            "status": run.status.value,
            "at": datetime.now(UTC).isoformat(),
            "stage": "final",
        }
        yield f"event: run\ndata: {json.dumps(final_payload)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
