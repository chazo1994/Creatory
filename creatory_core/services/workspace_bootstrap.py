from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.db.models import (
    Agent,
    NodeType,
    WorkflowEdge,
    WorkflowNode,
    WorkflowTemplate,
    Workspace,
)
from creatory_core.services.workflow_catalog import (
    WorkflowTemplateLoadError,
    load_template_file,
)


DIRECTOR_AGENT_SLUG = "main-director"


NODE_KIND_MAP = {
    "agent": NodeType.AGENT,
    "tool": NodeType.TOOL,
    "human_gate": NodeType.HUMAN_GATE,
    "router": NodeType.ROUTER,
    "memory": NodeType.MEMORY,
}


def _load_starter_template_definition() -> dict:
    try:
        return load_template_file("short_video_pipeline.yaml")
    except WorkflowTemplateLoadError:
        # Keep a resilient fallback for bootstrap environments.
        return {
            "name": "Short Video Pipeline",
            "description": "Starter agentic pipeline for short-form content production.",
            "version": 1,
            "definition_json": {
                "objective": "Transform an idea into a ready-to-publish short video package",
                "category": "short-form",
            },
            "nodes": [
                {
                    "node_key": "research",
                    "type": "agent",
                    "config_json": {"agent": "trend-researcher"},
                    "position_x": 60,
                    "position_y": 120,
                },
                {
                    "node_key": "script",
                    "type": "agent",
                    "config_json": {"agent": "script-writer"},
                    "position_x": 320,
                    "position_y": 120,
                },
                {
                    "node_key": "visuals",
                    "type": "tool",
                    "config_json": {"tool_group": "image-video-gen"},
                    "position_x": 580,
                    "position_y": 120,
                },
                {
                    "node_key": "human_review",
                    "type": "human_gate",
                    "config_json": {"required": True, "label": "Creator Review"},
                    "position_x": 840,
                    "position_y": 120,
                },
            ],
            "edges": [
                {
                    "source_node_key": "research",
                    "target_node_key": "script",
                    "metadata_json": {},
                },
                {
                    "source_node_key": "script",
                    "target_node_key": "visuals",
                    "metadata_json": {},
                },
                {
                    "source_node_key": "visuals",
                    "target_node_key": "human_review",
                    "metadata_json": {},
                },
            ],
        }


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

    starter_template = _load_starter_template_definition()
    template_name = str(starter_template.get("name") or "Short Video Pipeline")
    template_version = int(starter_template.get("version") or 1)

    existing_template = await db.scalar(
        select(WorkflowTemplate).where(
            WorkflowTemplate.workspace_id == workspace.id,
            WorkflowTemplate.name == template_name,
            WorkflowTemplate.version == template_version,
        )
    )
    if existing_template is not None:
        return

    template = WorkflowTemplate(
        workspace_id=workspace.id,
        name=template_name,
        description=str(
            starter_template.get("description")
            or "Starter agentic pipeline for short-form content production."
        ),
        version=template_version,
        is_public=False,
        definition_json=dict(starter_template.get("definition_json") or {}),
        created_by=workspace.owner_id,
    )
    db.add(template)
    await db.flush()

    nodes = []
    for item in list(starter_template.get("nodes") or []):
        node_type = NODE_KIND_MAP.get(str(item.get("type") or "").lower())
        if node_type is None:
            continue
        node_key = str(item.get("node_key") or "").strip()
        if not node_key:
            continue

        nodes.append(
            WorkflowNode(
                template_id=template.id,
                node_key=node_key,
                type=node_type,
                config_json=dict(item.get("config_json") or {}),
                position_x=item.get("position_x"),
                position_y=item.get("position_y"),
            )
        )
    db.add_all(nodes)

    edges = []
    for item in list(starter_template.get("edges") or []):
        source_key = str(item.get("source_node_key") or "").strip()
        target_key = str(item.get("target_node_key") or "").strip()
        if not source_key or not target_key:
            continue
        edges.append(
            WorkflowEdge(
                template_id=template.id,
                source_node_key=source_key,
                target_node_key=target_key,
                condition_expr=item.get("condition_expr"),
                metadata_json=dict(item.get("metadata_json") or {}),
            )
        )
    db.add_all(edges)
