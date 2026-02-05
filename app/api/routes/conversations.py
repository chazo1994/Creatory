import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.api.permissions import (
    ensure_conversation_member,
    ensure_thread_in_conversation,
    ensure_workspace_member,
)
from app.db.models import ContextInjection, Conversation, Message, Thread, ThreadKind, User
from app.db.session import get_db_session
from app.schemas.conversation import (
    ContextInjectionCreateRequest,
    ContextInjectionRead,
    ConversationCreateRequest,
    ConversationRead,
    MessageCreateRequest,
    MessageRead,
    ThreadCreateRequest,
    ThreadRead,
)

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    payload: ConversationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ConversationRead:
    await ensure_workspace_member(db, payload.workspace_id, current_user.id)

    conversation = Conversation(
        workspace_id=payload.workspace_id,
        creator_id=current_user.id,
        title=payload.title,
    )
    db.add(conversation)
    await db.flush()

    # Every conversation starts with a main thread and one quick side thread.
    db.add(
        Thread(
            conversation_id=conversation.id,
            kind=ThreadKind.MAIN,
            parent_thread_id=None,
            created_by=current_user.id,
        )
    )
    db.add(
        Thread(
            conversation_id=conversation.id,
            kind=ThreadKind.QUICK,
            parent_thread_id=None,
            created_by=current_user.id,
        )
    )

    await db.commit()
    await db.refresh(conversation)
    return ConversationRead.model_validate(conversation)


@router.get("", response_model=list[ConversationRead])
async def list_conversations(
    workspace_id: uuid.UUID,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[ConversationRead]:
    await ensure_workspace_member(db, workspace_id, current_user.id)

    result = await db.scalars(
        select(Conversation)
        .where(Conversation.workspace_id == workspace_id)
        .order_by(Conversation.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return [ConversationRead.model_validate(item) for item in result.all()]


@router.post(
    "/{conversation_id}/threads",
    response_model=ThreadRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_thread(
    conversation_id: uuid.UUID,
    payload: ThreadCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ThreadRead:
    conversation = await ensure_conversation_member(db, conversation_id, current_user.id)

    if payload.parent_thread_id is not None:
        await ensure_thread_in_conversation(db, payload.parent_thread_id, conversation.id)

    thread = Thread(
        conversation_id=conversation_id,
        kind=payload.kind,
        parent_thread_id=payload.parent_thread_id,
        created_by=current_user.id,
    )
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return ThreadRead.model_validate(thread)


@router.get("/{conversation_id}/threads", response_model=list[ThreadRead])
async def list_threads(
    conversation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[ThreadRead]:
    await ensure_conversation_member(db, conversation_id, current_user.id)

    result = await db.scalars(
        select(Thread)
        .where(Thread.conversation_id == conversation_id)
        .order_by(Thread.created_at.asc())
    )
    return [ThreadRead.model_validate(item) for item in result.all()]


@router.post("/{conversation_id}/threads/{thread_id}/messages", response_model=MessageRead)
async def create_message(
    conversation_id: uuid.UUID,
    thread_id: uuid.UUID,
    payload: MessageCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MessageRead:
    await ensure_conversation_member(db, conversation_id, current_user.id)
    await ensure_thread_in_conversation(db, thread_id, conversation_id)

    message = Message(
        thread_id=thread_id,
        role=payload.role,
        content_json=payload.content_json,
        token_count=payload.token_count,
        created_by=current_user.id,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return MessageRead.model_validate(message)


@router.get("/{conversation_id}/threads/{thread_id}/messages", response_model=list[MessageRead])
async def list_messages(
    conversation_id: uuid.UUID,
    thread_id: uuid.UUID,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[MessageRead]:
    await ensure_conversation_member(db, conversation_id, current_user.id)
    await ensure_thread_in_conversation(db, thread_id, conversation_id)

    result = await db.scalars(
        select(Message)
        .where(Message.thread_id == thread_id)
        .order_by(Message.created_at.asc())
        .limit(limit)
        .offset(offset)
    )
    return [MessageRead.model_validate(item) for item in result.all()]


@router.post(
    "/{conversation_id}/inject",
    response_model=ContextInjectionRead,
    status_code=status.HTTP_201_CREATED,
)
async def inject_context(
    conversation_id: uuid.UUID,
    payload: ContextInjectionCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ContextInjectionRead:
    await ensure_conversation_member(db, conversation_id, current_user.id)
    await ensure_thread_in_conversation(db, payload.from_thread_id, conversation_id)
    await ensure_thread_in_conversation(db, payload.to_thread_id, conversation_id)

    from_message = await db.get(Message, payload.from_message_id)
    if from_message is None or from_message.thread_id != payload.from_thread_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source message not found",
        )

    if payload.to_message_id:
        to_message = await db.get(Message, payload.to_message_id)
        if to_message is None or to_message.thread_id != payload.to_thread_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target message not found",
            )

    injection = ContextInjection(
        conversation_id=conversation_id,
        from_thread_id=payload.from_thread_id,
        from_message_id=payload.from_message_id,
        to_thread_id=payload.to_thread_id,
        to_message_id=payload.to_message_id,
        context_block=payload.context_block,
        injected_by=current_user.id,
    )
    db.add(injection)
    await db.commit()
    await db.refresh(injection)
    return ContextInjectionRead.model_validate(injection)
