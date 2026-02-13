import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.api.deps import get_current_user
from creatory_core.api.permissions import ensure_workspace_member
from creatory_core.db.models import Agent, AgentRun, User
from creatory_core.db.session import get_db_session
from creatory_core.schemas.agent import AgentCreateRequest, AgentRead, AgentRunRead

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
async def create_agent(
    payload: AgentCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> AgentRead:
    if payload.workspace_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="workspace_id is required",
        )

    await ensure_workspace_member(db, payload.workspace_id, current_user.id)

    agent = Agent(
        workspace_id=payload.workspace_id,
        slug=payload.slug,
        display_name=payload.display_name,
        persona_prompt=payload.persona_prompt,
        config_json=payload.config_json,
        is_system=payload.is_system,
    )
    db.add(agent)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Agent slug already exists in this workspace",
        ) from None

    await db.refresh(agent)
    return AgentRead.model_validate(agent)


@router.get("", response_model=list[AgentRead])
async def list_agents(
    workspace_id: uuid.UUID,
    include_system: bool = Query(default=True),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[AgentRead]:
    await ensure_workspace_member(db, workspace_id, current_user.id)

    query = select(Agent).where(Agent.workspace_id == workspace_id)
    if include_system:
        query = select(Agent).where(
            or_(
                Agent.workspace_id == workspace_id,
                (Agent.workspace_id.is_(None) & (Agent.is_system.is_(True))),
            )
        )

    result = await db.scalars(query.order_by(Agent.created_at.desc()).limit(limit).offset(offset))
    return [AgentRead.model_validate(item) for item in result.all()]


@router.get("/{agent_id}", response_model=AgentRead)
async def get_agent(
    agent_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> AgentRead:
    agent = await db.get(Agent, agent_id)
    if agent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

    if agent.workspace_id is not None:
        await ensure_workspace_member(db, agent.workspace_id, current_user.id)

    return AgentRead.model_validate(agent)


@router.get("/{agent_id}/runs", response_model=list[AgentRunRead])
async def list_agent_runs(
    agent_id: uuid.UUID,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[AgentRunRead]:
    agent = await db.get(Agent, agent_id)
    if agent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

    if agent.workspace_id is not None:
        await ensure_workspace_member(db, agent.workspace_id, current_user.id)

    result = await db.scalars(
        select(AgentRun)
        .where(AgentRun.agent_id == agent_id)
        .order_by(AgentRun.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return [AgentRunRead.model_validate(item) for item in result.all()]
