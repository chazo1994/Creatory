from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.core.config import settings
from creatory_core.db.models import (
    NodeType,
    RunStatus,
    WorkflowNode,
    WorkflowRun,
    WorkflowRunStep,
    WorkflowTemplate,
)
from creatory_core.services.circuit_breaker import (
    CircuitBreakerConfig,
    CircuitBreakerTriggered,
    assert_step_budget,
)


async def run_workflow(
    db: AsyncSession,
    template: WorkflowTemplate,
    created_by,
    conversation_id,
    input_json: dict,
) -> tuple[WorkflowRun, list[WorkflowRunStep]]:
    now = datetime.now(UTC)
    workflow_run = WorkflowRun(
        template_id=template.id,
        conversation_id=conversation_id,
        status=RunStatus.RUNNING,
        input_json=input_json,
        output_json={},
        started_at=now,
        created_by=created_by,
    )
    db.add(workflow_run)
    await db.flush()

    nodes = (
        await db.scalars(
            select(WorkflowNode)
            .where(WorkflowNode.template_id == template.id)
            .order_by(WorkflowNode.position_x.asc().nullslast(), WorkflowNode.node_key.asc())
        )
    ).all()

    steps: list[WorkflowRunStep] = []
    run_status = RunStatus.SUCCEEDED

    try:
        assert_step_budget(
            requested_steps=len(nodes),
            config=CircuitBreakerConfig(max_steps=settings.circuit_breaker_max_steps),
        )
    except CircuitBreakerTriggered as exc:
        workflow_run.status = RunStatus.FAILED
        workflow_run.output_json = {
            "steps_completed": 0,
            "steps_total": len(nodes),
            "final_status": RunStatus.FAILED.value,
        }
        workflow_run.ended_at = datetime.now(UTC)
        await db.commit()
        await db.refresh(workflow_run)
        raise exc

    for node in nodes:
        step_started = datetime.now(UTC)
        step = WorkflowRunStep(
            workflow_run_id=workflow_run.id,
            node_key=node.node_key,
            status=RunStatus.RUNNING,
            input_json={"node": node.node_key, "type": node.type.value},
            output_json={},
            started_at=step_started,
            attempt=1,
        )
        db.add(step)
        await db.flush()

        if node.type == NodeType.HUMAN_GATE:
            step.status = RunStatus.WAITING_HUMAN
            step.output_json = {
                "message": "Awaiting creator confirmation before continuing.",
                "human_gate": True,
            }
            step.ended_at = datetime.now(UTC)
            run_status = RunStatus.WAITING_HUMAN
            steps.append(step)
            break

        step.status = RunStatus.SUCCEEDED
        step.output_json = {
            "message": f"Node {node.node_key} executed successfully",
            "summary": {
                "agentic": node.type in {NodeType.AGENT, NodeType.TOOL},
                "config": node.config_json,
            },
        }
        step.ended_at = datetime.now(UTC)
        steps.append(step)

    workflow_run.status = run_status
    workflow_run.output_json = {
        "steps_completed": len(steps),
        "steps_total": len(nodes),
        "final_status": run_status.value,
    }
    if run_status != RunStatus.WAITING_HUMAN:
        workflow_run.ended_at = datetime.now(UTC)

    await db.commit()
    await db.refresh(workflow_run)
    for step in steps:
        await db.refresh(step)

    return workflow_run, steps
