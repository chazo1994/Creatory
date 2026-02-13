import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.api.deps import get_current_user
from creatory_core.api.permissions import ensure_conversation_member, ensure_workspace_member
from creatory_core.db.models import (
    User,
    WorkflowEdge,
    WorkflowNode,
    WorkflowRun,
    WorkflowRunStep,
    WorkflowTemplate,
)
from creatory_core.db.session import get_db_session
from creatory_core.schemas.workflow import (
    WorkflowEdgeRead,
    WorkflowNodeRead,
    WorkflowRunCreateRequest,
    WorkflowRunDetail,
    WorkflowRunStepRead,
    WorkflowTemplateCreateRequest,
    WorkflowTemplateDetail,
    WorkflowTemplateRead,
)
from creatory_core.services.circuit_breaker import CircuitBreakerTriggered
from creatory_core.services.workflow_runner import run_workflow

router = APIRouter(prefix="/workflows", tags=["workflows"])


async def _template_detail(db: AsyncSession, template: WorkflowTemplate) -> WorkflowTemplateDetail:
    nodes = (
        await db.scalars(
            select(WorkflowNode)
            .where(WorkflowNode.template_id == template.id)
            .order_by(WorkflowNode.position_x.asc().nullslast(), WorkflowNode.node_key.asc())
        )
    ).all()

    edges = (
        await db.scalars(
            select(WorkflowEdge)
            .where(WorkflowEdge.template_id == template.id)
            .order_by(WorkflowEdge.source_node_key.asc(), WorkflowEdge.target_node_key.asc())
        )
    ).all()

    detail = WorkflowTemplateDetail.model_validate(template)
    detail.nodes = [WorkflowNodeRead.model_validate(item) for item in nodes]
    detail.edges = [WorkflowEdgeRead.model_validate(item) for item in edges]
    return detail


async def _template_for_user_or_404(
    db: AsyncSession,
    template_id: uuid.UUID,
    user_id: uuid.UUID,
) -> WorkflowTemplate:
    template = await db.get(WorkflowTemplate, template_id)
    if template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow template not found",
        )

    await ensure_workspace_member(db, template.workspace_id, user_id)
    return template


@router.post(
    "/templates",
    response_model=WorkflowTemplateDetail,
    status_code=status.HTTP_201_CREATED,
)
async def create_template(
    payload: WorkflowTemplateCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> WorkflowTemplateDetail:
    await ensure_workspace_member(db, payload.workspace_id, current_user.id)

    template = WorkflowTemplate(
        workspace_id=payload.workspace_id,
        name=payload.name,
        description=payload.description,
        version=payload.version,
        is_public=payload.is_public,
        definition_json=payload.definition_json,
        created_by=current_user.id,
    )
    db.add(template)
    await db.flush()

    db.add_all(
        [
            WorkflowNode(
                template_id=template.id,
                node_key=node.node_key,
                type=node.type,
                config_json=node.config_json,
                position_x=node.position_x,
                position_y=node.position_y,
            )
            for node in payload.nodes
        ]
    )
    db.add_all(
        [
            WorkflowEdge(
                template_id=template.id,
                source_node_key=edge.source_node_key,
                target_node_key=edge.target_node_key,
                condition_expr=edge.condition_expr,
                metadata_json=edge.metadata_json,
            )
            for edge in payload.edges
        ]
    )

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Template name/version already exists in this workspace",
        ) from None

    await db.refresh(template)
    return await _template_detail(db, template)


@router.get("/templates", response_model=list[WorkflowTemplateRead])
async def list_templates(
    workspace_id: uuid.UUID,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[WorkflowTemplateRead]:
    await ensure_workspace_member(db, workspace_id, current_user.id)

    result = await db.scalars(
        select(WorkflowTemplate)
        .where(WorkflowTemplate.workspace_id == workspace_id)
        .order_by(WorkflowTemplate.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return [WorkflowTemplateRead.model_validate(item) for item in result.all()]


@router.get("/templates/{template_id}", response_model=WorkflowTemplateDetail)
async def get_template(
    template_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> WorkflowTemplateDetail:
    template = await _template_for_user_or_404(db, template_id, current_user.id)
    return await _template_detail(db, template)


@router.post(
    "/templates/{template_id}/run",
    response_model=WorkflowRunDetail,
    status_code=status.HTTP_201_CREATED,
)
async def run_template(
    template_id: uuid.UUID,
    payload: WorkflowRunCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> WorkflowRunDetail:
    template = await _template_for_user_or_404(db, template_id, current_user.id)

    if payload.conversation_id is not None:
        conversation = await ensure_conversation_member(
            db,
            payload.conversation_id,
            current_user.id,
        )
        if conversation.workspace_id != template.workspace_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conversation and template must belong to the same workspace",
            )

    try:
        workflow_run, steps = await run_workflow(
            db=db,
            template=template,
            created_by=current_user.id,
            conversation_id=payload.conversation_id,
            input_json=payload.input_json,
        )
    except CircuitBreakerTriggered as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    response = WorkflowRunDetail.model_validate(workflow_run)
    response.steps = [WorkflowRunStepRead.model_validate(step) for step in steps]
    return response


@router.get("/runs/{workflow_run_id}", response_model=WorkflowRunDetail)
async def get_run(
    workflow_run_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> WorkflowRunDetail:
    workflow_run = await db.get(WorkflowRun, workflow_run_id)
    if workflow_run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow run not found")

    template = await db.get(WorkflowTemplate, workflow_run.template_id)
    if template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow template not found",
        )
    await ensure_workspace_member(db, template.workspace_id, current_user.id)

    steps = (
        await db.scalars(
            select(WorkflowRunStep)
            .where(WorkflowRunStep.workflow_run_id == workflow_run.id)
            .order_by(WorkflowRunStep.created_at.asc())
        )
    ).all()

    response = WorkflowRunDetail.model_validate(workflow_run)
    response.steps = [WorkflowRunStepRead.model_validate(step) for step in steps]
    return response


@router.get("/runs/{workflow_run_id}/steps", response_model=list[WorkflowRunStepRead])
async def list_run_steps(
    workflow_run_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[WorkflowRunStepRead]:
    workflow_run = await db.get(WorkflowRun, workflow_run_id)
    if workflow_run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow run not found")

    template = await db.get(WorkflowTemplate, workflow_run.template_id)
    if template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow template not found",
        )
    await ensure_workspace_member(db, template.workspace_id, current_user.id)

    steps = (
        await db.scalars(
            select(WorkflowRunStep)
            .where(WorkflowRunStep.workflow_run_id == workflow_run.id)
            .order_by(WorkflowRunStep.created_at.asc())
        )
    ).all()
    return [WorkflowRunStepRead.model_validate(step) for step in steps]
