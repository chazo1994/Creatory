import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.api.permissions import ensure_workspace_member
from app.db.models import MediaAsset, User
from app.db.session import get_db_session
from app.schemas.media import MediaAssetCreateRequest, MediaAssetRead

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("", response_model=MediaAssetRead, status_code=status.HTTP_201_CREATED)
async def create_asset(
    payload: MediaAssetCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MediaAssetRead:
    await ensure_workspace_member(db, payload.workspace_id, current_user.id)

    asset = MediaAsset(
        workspace_id=payload.workspace_id,
        owner_id=current_user.id,
        type=payload.type,
        storage_uri=payload.storage_uri,
        source_message_id=payload.source_message_id,
        source_tool_invocation_id=payload.source_tool_invocation_id,
        metadata_json=payload.metadata_json,
    )
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return MediaAssetRead.model_validate(asset)


@router.get("", response_model=list[MediaAssetRead])
async def list_assets(
    workspace_id: uuid.UUID,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[MediaAssetRead]:
    await ensure_workspace_member(db, workspace_id, current_user.id)

    result = await db.scalars(
        select(MediaAsset)
        .where(MediaAsset.workspace_id == workspace_id)
        .order_by(MediaAsset.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return [MediaAssetRead.model_validate(item) for item in result.all()]
