import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.utils import slugify
from app.db.models import MembershipRole, User, Workspace, WorkspaceMembership
from app.db.session import get_db_session
from app.schemas.workspace import WorkspaceCreateRequest, WorkspaceRead
from app.services.workspace_bootstrap import bootstrap_workspace_defaults

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


async def _slug_exists(db: AsyncSession, slug: str) -> bool:
    return await db.scalar(select(Workspace.id).where(Workspace.slug == slug)) is not None


async def _generate_unique_slug(db: AsyncSession, source: str) -> str:
    base = slugify(source) or f"workspace-{uuid.uuid4().hex[:8]}"
    candidate = base
    counter = 1
    while await _slug_exists(db, candidate):
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate


@router.post("", response_model=WorkspaceRead, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    payload: WorkspaceCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> WorkspaceRead:
    slug_source = payload.slug or payload.name
    slug = await _generate_unique_slug(db, slug_source)

    workspace = Workspace(name=payload.name, slug=slug, owner_id=current_user.id)
    db.add(workspace)
    await db.flush()

    membership = WorkspaceMembership(
        workspace_id=workspace.id,
        user_id=current_user.id,
        role=MembershipRole.OWNER,
    )
    db.add(membership)

    await bootstrap_workspace_defaults(db, workspace)

    await db.commit()
    await db.refresh(workspace)
    return WorkspaceRead.model_validate(workspace)


@router.get("", response_model=list[WorkspaceRead])
async def list_workspaces(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[WorkspaceRead]:
    result = await db.scalars(
        select(Workspace)
        .join(WorkspaceMembership, WorkspaceMembership.workspace_id == Workspace.id)
        .where(WorkspaceMembership.user_id == current_user.id)
        .order_by(Workspace.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return [WorkspaceRead.model_validate(item) for item in result.all()]


@router.get("/{workspace_id}", response_model=WorkspaceRead)
async def get_workspace(
    workspace_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> WorkspaceRead:
    membership = await db.scalar(
        select(WorkspaceMembership).where(
            WorkspaceMembership.workspace_id == workspace_id,
            WorkspaceMembership.user_id == current_user.id,
        )
    )
    if membership is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    workspace = await db.get(Workspace, workspace_id)
    if workspace is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    return WorkspaceRead.model_validate(workspace)
