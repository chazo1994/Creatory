from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.db.models import ContextInjection, Message, MessageRole


@dataclass(frozen=True)
class BridgeInjectionResult:
    context_injection: ContextInjection
    bridge_message: Message


def normalize_context_block(source_message: Message, payload_block: dict) -> dict:
    extracted_text = payload_block.get("text")
    if not isinstance(extracted_text, str) or not extracted_text.strip():
        source_text = source_message.content_json.get("text")
        extracted_text = source_text if isinstance(source_text, str) else str(source_message.content_json)

    return {
        "reference_id": payload_block.get("reference_id") or str(source_message.id),
        "text": extracted_text.strip(),
        "source": payload_block.get("source") or "quick-thread",
        "metadata": payload_block.get("metadata") or {},
    }


async def inject_context_block(
    db: AsyncSession,
    *,
    conversation_id: UUID,
    from_thread_id: UUID,
    from_message: Message,
    to_thread_id: UUID,
    to_message_id: UUID | None,
    injected_by: UUID,
    payload_context_block: dict,
) -> BridgeInjectionResult:
    normalized_block = normalize_context_block(from_message, payload_context_block)

    bridge_message = Message(
        thread_id=to_thread_id,
        role=MessageRole.SYSTEM,
        content_json={
            "text": (
                "Context injected from quick stream. Use this block as verified side-thread input "
                "for the next director turn."
            ),
            "context_block": normalized_block,
            "bridge": {
                "from_thread_id": str(from_thread_id),
                "from_message_id": str(from_message.id),
                "mode": "bridge_injector",
            },
        },
        created_by=injected_by,
    )
    db.add(bridge_message)
    await db.flush()

    context_injection = ContextInjection(
        conversation_id=conversation_id,
        from_thread_id=from_thread_id,
        from_message_id=from_message.id,
        to_thread_id=to_thread_id,
        to_message_id=to_message_id or bridge_message.id,
        context_block=normalized_block,
        injected_by=injected_by,
    )
    db.add(context_injection)
    await db.flush()

    return BridgeInjectionResult(
        context_injection=context_injection,
        bridge_message=bridge_message,
    )
