from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.core.config import settings
from creatory_core.db.models import (
    Agent,
    AgentRun,
    Conversation,
    Message,
    MessageRole,
    RunStatus,
    Task,
    Thread,
    ThreadKind,
    User,
)
from creatory_core.providers.router import route_for_task
from creatory_core.schemas.orchestrator import ChatRunRequest
from creatory_core.services.circuit_breaker import (
    CircuitBreakerConfig,
    assert_step_budget,
)
from creatory_core.services.workspace_bootstrap import DIRECTOR_AGENT_SLUG


@dataclass
class DirectorTurnResult:
    user_message: Message
    assistant_message: Message
    agent_run: AgentRun
    tasks: list[Task]


async def _resolve_agent(
    db: AsyncSession,
    workspace_id,
    assistant_agent_slug: str | None,
) -> Agent | None:
    if assistant_agent_slug:
        return await db.scalar(
            select(Agent).where(
                Agent.workspace_id == workspace_id,
                Agent.slug == assistant_agent_slug,
            )
        )

    return await db.scalar(
        select(Agent).where(
            Agent.workspace_id == workspace_id,
            Agent.slug == DIRECTOR_AGENT_SLUG,
        )
    )


def _build_plan(prompt: str, thread_kind: ThreadKind) -> list[str]:
    intent = prompt.strip()
    if thread_kind == ThreadKind.QUICK:
        return [
            f"Directly answer quick request: {intent[:80]}",
            "Return concise recommendation with optional next action",
        ]

    return [
        "Decode creator intention and target audience",
        "Draft content structure: hook, value, CTA",
        "Select suitable tools for script/media generation",
        "Create production checklist for human review",
    ]


def _assistant_text(prompt: str, thread_kind: ThreadKind, plan: list[str]) -> str:
    if thread_kind == ThreadKind.QUICK:
        return (
            "Quick answer prepared.\n\n"
            f"Question: {prompt.strip()}\n"
            "Recommendation: Use this as a scoped experiment, then inject into main thread "
            "if approved."
        )

    lines = [
        "Director coordination initialized.",
        "",
        f"Input idea: {prompt.strip()}",
        "",
        "Execution plan:",
    ]
    for index, step in enumerate(plan, start=1):
        lines.append(f"{index}. {step}")

    lines.append("")
    routing = route_for_task(prompt, prefer_local=False)
    lines.append("Provider routing:")
    lines.append(f"- Draft model route: {routing.draft_provider}")
    lines.append(f"- Refinement model route: {routing.refine_provider}")
    lines.append(f"- Why: {routing.reason}")
    lines.append("")
    lines.append("Next: choose tools for script, visuals, and voice-over, then run a draft pipeline.")
    return "\n".join(lines)


async def run_director_turn(
    db: AsyncSession,
    current_user: User,
    conversation: Conversation,
    thread: Thread,
    payload: ChatRunRequest,
) -> DirectorTurnResult:
    user_message = Message(
        thread_id=thread.id,
        role=MessageRole.USER,
        content_json={
            "text": payload.prompt,
            "metadata": payload.metadata_json,
        },
        created_by=current_user.id,
    )
    db.add(user_message)
    await db.flush()

    agent = await _resolve_agent(db, conversation.workspace_id, payload.assistant_agent_slug)
    if agent is None:
        agent = Agent(
            workspace_id=conversation.workspace_id,
            slug=DIRECTOR_AGENT_SLUG,
            display_name="Main Director Agent",
            persona_prompt=(
                "Coordinate creator workflows end-to-end. Plan tasks, orchestrate tools, and "
                "keep human-in-the-loop checkpoints."
            ),
            config_json={"mode": "director"},
            is_system=True,
        )
        db.add(agent)
        await db.flush()

    run_started = datetime.now(UTC)
    run = AgentRun(
        conversation_id=conversation.id,
        thread_id=thread.id,
        agent_id=agent.id,
        status=RunStatus.RUNNING,
        input_json={
            "prompt": payload.prompt,
            "thread_kind": thread.kind.value,
            "metadata": payload.metadata_json,
        },
        output_json={},
        started_at=run_started,
    )
    db.add(run)
    await db.flush()

    plan = _build_plan(payload.prompt, thread.kind)
    assert_step_budget(
        requested_steps=len(plan),
        config=CircuitBreakerConfig(max_steps=settings.circuit_breaker_max_steps),
    )
    routing = route_for_task(payload.prompt, prefer_local=False)

    planning_task = Task(
        agent_run_id=run.id,
        task_type="planning",
        status=RunStatus.SUCCEEDED,
        input_json={"prompt": payload.prompt},
        output_json={
            "plan": plan,
            "provider_routing": {
                "draft_provider": routing.draft_provider,
                "refine_provider": routing.refine_provider,
                "reason": routing.reason,
            },
        },
        started_at=run_started,
        ended_at=datetime.now(UTC),
    )
    db.add(planning_task)
    await db.flush()

    content_task = Task(
        agent_run_id=run.id,
        parent_task_id=planning_task.id,
        task_type="draft_content",
        status=RunStatus.SUCCEEDED,
        input_json={"plan": plan},
        output_json={
            "draft_kind": "quick_reply" if thread.kind == ThreadKind.QUICK else "structured_outline",
            "draft_provider": routing.draft_provider,
            "refine_provider": routing.refine_provider,
        },
        started_at=datetime.now(UTC),
        ended_at=datetime.now(UTC),
    )
    db.add(content_task)

    assistant_message = Message(
        thread_id=thread.id,
        role=MessageRole.ASSISTANT,
        content_json={
            "text": _assistant_text(payload.prompt, thread.kind, plan),
            "plan": plan,
            "agent": {
                "id": str(agent.id),
                "slug": agent.slug,
                "display_name": agent.display_name,
            },
            "provider_routing": {
                "draft_provider": routing.draft_provider,
                "refine_provider": routing.refine_provider,
                "reason": routing.reason,
            },
        },
        created_by=None,
    )
    db.add(assistant_message)
    await db.flush()

    run.status = RunStatus.SUCCEEDED
    run.output_json = {
        "assistant_message_id": str(assistant_message.id),
        "plan": plan,
        "provider_routing": {
            "draft_provider": routing.draft_provider,
            "refine_provider": routing.refine_provider,
            "reason": routing.reason,
        },
        "tasks": ["planning", "draft_content"],
    }
    run.ended_at = datetime.now(UTC)

    await db.commit()
    await db.refresh(user_message)
    await db.refresh(assistant_message)
    await db.refresh(run)
    await db.refresh(planning_task)
    await db.refresh(content_task)

    return DirectorTurnResult(
        user_message=user_message,
        assistant_message=assistant_message,
        agent_run=run,
        tasks=[planning_task, content_task],
    )
