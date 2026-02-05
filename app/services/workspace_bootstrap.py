from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    Agent,
    NodeType,
    WorkflowEdge,
    WorkflowNode,
    WorkflowTemplate,
    Workspace,
)


DIRECTOR_AGENT_SLUG = "main-director"


async def bootstrap_workspace_defaults(
    db: AsyncSession,
    workspace: Workspace,
) -> None:
    existing_director = await db.scalar(
        select(Agent).where(
            Agent.workspace_id == workspace.id,
            Agent.slug == DIRECTOR_AGENT_SLUG,
        )
    )
    if existing_director is None:
        db.add(
            Agent(
                workspace_id=workspace.id,
                slug=DIRECTOR_AGENT_SLUG,
                display_name="Main Director Agent",
                persona_prompt=(
                    "You are the central coordinator for creator workflows. "
                    "Break ideas into concrete "
                    "tasks, propose tool calls, and keep outputs ready for publishing."
                ),
                config_json={
                    "mode": "director",
                    "supports_dual_stream": True,
                    "supports_injection": True,
                },
                is_system=True,
            )
        )

    existing_template = await db.scalar(
        select(WorkflowTemplate).where(
            WorkflowTemplate.workspace_id == workspace.id,
            WorkflowTemplate.name == "Short Video Pipeline",
            WorkflowTemplate.version == 1,
        )
    )
    if existing_template is not None:
        return

    template = WorkflowTemplate(
        workspace_id=workspace.id,
        name="Short Video Pipeline",
        description="Starter agentic pipeline for short-form content production.",
        version=1,
        is_public=False,
        definition_json={
            "objective": "Transform an idea into a ready-to-publish short video package",
            "category": "short-form",
        },
        created_by=workspace.owner_id,
    )
    db.add(template)
    await db.flush()

    nodes = [
        WorkflowNode(
            template_id=template.id,
            node_key="research",
            type=NodeType.AGENT,
            config_json={"agent": "trend-researcher"},
            position_x=60,
            position_y=120,
        ),
        WorkflowNode(
            template_id=template.id,
            node_key="script",
            type=NodeType.AGENT,
            config_json={"agent": "script-writer"},
            position_x=320,
            position_y=120,
        ),
        WorkflowNode(
            template_id=template.id,
            node_key="visuals",
            type=NodeType.TOOL,
            config_json={"tool_group": "image-video-gen"},
            position_x=580,
            position_y=120,
        ),
        WorkflowNode(
            template_id=template.id,
            node_key="human_review",
            type=NodeType.HUMAN_GATE,
            config_json={"required": True, "label": "Creator Review"},
            position_x=840,
            position_y=120,
        ),
    ]
    db.add_all(nodes)

    edges = [
        WorkflowEdge(
            template_id=template.id,
            source_node_key="research",
            target_node_key="script",
            metadata_json={},
        ),
        WorkflowEdge(
            template_id=template.id,
            source_node_key="script",
            target_node_key="visuals",
            metadata_json={},
        ),
        WorkflowEdge(
            template_id=template.id,
            source_node_key="visuals",
            target_node_key="human_review",
            metadata_json={},
        ),
    ]
    db.add_all(edges)
