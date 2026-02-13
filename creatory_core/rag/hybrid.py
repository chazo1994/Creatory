from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.db.models import ConceptNode, KnowledgeChunk, KnowledgeSource


@dataclass(frozen=True)
class RetrievedContext:
    chunk_id: UUID
    source_id: UUID
    source_title: str | None
    content: str
    score: float
    citation_index: int


class HybridRAGService:
    """Bootstrap hybrid retrieval: lexical chunk ranking + concept graph boost."""

    async def retrieve(
        self,
        db: AsyncSession,
        workspace_id: UUID,
        query: str,
        *,
        top_k: int = 5,
    ) -> list[RetrievedContext]:
        normalized_query = query.strip().lower()
        if not normalized_query:
            return []

        chunks = (
            await db.execute(
                select(KnowledgeChunk, KnowledgeSource)
                .join(KnowledgeSource, KnowledgeChunk.source_id == KnowledgeSource.id)
                .where(KnowledgeSource.workspace_id == workspace_id)
                .order_by(KnowledgeSource.created_at.desc(), KnowledgeChunk.chunk_index.asc())
                .limit(200)
            )
        ).all()

        concept_bonus = await self._concept_bonus(db, workspace_id, normalized_query)

        scored: list[RetrievedContext] = []
        for chunk, source in chunks:
            score = self._chunk_score(normalized_query, chunk.content)
            score += concept_bonus
            if score <= 0:
                continue
            scored.append(
                RetrievedContext(
                    chunk_id=chunk.id,
                    source_id=source.id,
                    source_title=source.title,
                    content=chunk.content,
                    score=score,
                    citation_index=0,
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        selected = scored[:top_k]

        return [
            RetrievedContext(
                chunk_id=item.chunk_id,
                source_id=item.source_id,
                source_title=item.source_title,
                content=item.content,
                score=item.score,
                citation_index=index,
            )
            for index, item in enumerate(selected, start=1)
        ]

    async def _concept_bonus(
        self,
        db: AsyncSession,
        workspace_id: UUID,
        query: str,
    ) -> float:
        tokens = self._tokens(query)
        if not tokens:
            return 0.0

        concepts = (
            await db.scalars(
                select(ConceptNode)
                .where(ConceptNode.workspace_id == workspace_id)
                .limit(400)
            )
        ).all()
        matches = 0
        for concept in concepts:
            hay = f"{concept.concept_key} {concept.label}".lower()
            if any(token in hay for token in tokens):
                matches += 1
        if matches == 0:
            return 0.0
        return min(0.35, 0.05 * matches)

    def _chunk_score(self, query: str, content: str) -> float:
        query_tokens = self._tokens(query)
        if not query_tokens:
            return 0.0

        content_lower = content.lower()
        hits = sum(1 for token in query_tokens if token in content_lower)
        if hits == 0:
            return 0.0

        density = hits / max(len(query_tokens), 1)
        length_penalty = 0.0 if len(content) <= 2000 else 0.05
        return max(0.0, density - length_penalty)

    def _tokens(self, text: str) -> list[str]:
        words = [word.strip(".,:;!?()[]{}\"'") for word in text.lower().split()]
        return [word for word in words if len(word) > 2]


def render_cited_answer(query: str, contexts: Iterable[RetrievedContext]) -> str:
    context_list = list(contexts)
    if not context_list:
        return (
            f"No direct RAG evidence found for: {query}\n"
            "Try uploading more sources or broadening your prompt."
        )

    summary_lines = [f"RAG notes for: {query}"]
    for item in context_list:
        source_title = item.source_title or "Untitled source"
        summary_lines.append(f"[{item.citation_index}] {source_title}: {item.content[:240]}")
    return "\n".join(summary_lines)
