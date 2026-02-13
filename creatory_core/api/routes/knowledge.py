import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.api.deps import get_current_user
from creatory_core.api.permissions import ensure_workspace_member
from creatory_core.db.models import KnowledgeChunk, KnowledgeSource, User
from creatory_core.db.session import get_db_session
from creatory_core.rag.hybrid import HybridRAGService, render_cited_answer
from creatory_core.schemas.knowledge import (
    KnowledgeChunkCreateRequest,
    KnowledgeChunkRead,
    KnowledgeCitation,
    KnowledgeQueryRequest,
    KnowledgeQueryResponse,
    KnowledgeSourceCreateRequest,
    KnowledgeSourceRead,
)

router = APIRouter(prefix="/knowledge", tags=["knowledge"])
rag_service = HybridRAGService()


@router.post("/sources", response_model=KnowledgeSourceRead, status_code=status.HTTP_201_CREATED)
async def create_source(
    payload: KnowledgeSourceCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> KnowledgeSourceRead:
    await ensure_workspace_member(db, payload.workspace_id, current_user.id)

    source = KnowledgeSource(
        workspace_id=payload.workspace_id,
        source_type=payload.source_type,
        uri=payload.uri,
        title=payload.title,
        metadata_json=payload.metadata_json,
        ingest_status="ready",
        created_by=current_user.id,
    )
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return KnowledgeSourceRead.model_validate(source)


@router.get("/sources", response_model=list[KnowledgeSourceRead])
async def list_sources(
    workspace_id: uuid.UUID,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[KnowledgeSourceRead]:
    await ensure_workspace_member(db, workspace_id, current_user.id)

    rows = (
        await db.scalars(
            select(KnowledgeSource)
            .where(KnowledgeSource.workspace_id == workspace_id)
            .order_by(KnowledgeSource.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
    ).all()

    return [KnowledgeSourceRead.model_validate(row) for row in rows]


@router.post(
    "/sources/{source_id}/chunks",
    response_model=KnowledgeChunkRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_chunk(
    source_id: uuid.UUID,
    payload: KnowledgeChunkCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> KnowledgeChunkRead:
    source = await db.get(KnowledgeSource, source_id)
    if source is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge source not found",
        )

    await ensure_workspace_member(db, source.workspace_id, current_user.id)

    next_index = await db.scalar(
        select(func.coalesce(func.max(KnowledgeChunk.chunk_index), -1) + 1).where(
            KnowledgeChunk.source_id == source.id
        )
    )

    chunk = KnowledgeChunk(
        source_id=source.id,
        chunk_index=int(next_index),
        content=payload.content,
        token_count=payload.token_count,
        metadata_json=payload.metadata_json,
    )
    db.add(chunk)
    await db.commit()
    await db.refresh(chunk)
    return KnowledgeChunkRead.model_validate(chunk)


@router.get("/sources/{source_id}/chunks", response_model=list[KnowledgeChunkRead])
async def list_chunks(
    source_id: uuid.UUID,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[KnowledgeChunkRead]:
    source = await db.get(KnowledgeSource, source_id)
    if source is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge source not found",
        )
    await ensure_workspace_member(db, source.workspace_id, current_user.id)

    rows = (
        await db.scalars(
            select(KnowledgeChunk)
            .where(KnowledgeChunk.source_id == source.id)
            .order_by(KnowledgeChunk.chunk_index.asc())
            .limit(limit)
            .offset(offset)
        )
    ).all()
    return [KnowledgeChunkRead.model_validate(row) for row in rows]


@router.post("/query", response_model=KnowledgeQueryResponse)
async def query_knowledge(
    payload: KnowledgeQueryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> KnowledgeQueryResponse:
    await ensure_workspace_member(db, payload.workspace_id, current_user.id)

    contexts = await rag_service.retrieve(
        db,
        payload.workspace_id,
        payload.query,
        top_k=payload.top_k,
    )

    citations = [
        KnowledgeCitation(
            index=item.citation_index,
            chunk_id=item.chunk_id,
            source_id=item.source_id,
            source_title=item.source_title,
            score=item.score,
            content=item.content,
        )
        for item in contexts
    ]

    return KnowledgeQueryResponse(
        query=payload.query,
        answer_preview=render_cited_answer(payload.query, contexts),
        citations=citations,
    )
