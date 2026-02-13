from fastapi import APIRouter, Depends

from creatory_core.api.deps import get_current_user
from creatory_core.db.models import User
from creatory_core.providers.base import ProviderKind
from creatory_core.providers.router import route_for_task
from creatory_core.providers.service import list_provider_specs, probe_provider_connection
from creatory_core.schemas.provider import (
    ProviderConnectionTestRequest,
    ProviderConnectionTestResponse,
    ProviderRead,
    ProviderRoutingPreviewRequest,
    ProviderRoutingPreviewResponse,
)

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("/catalog", response_model=list[ProviderRead])
async def list_catalog(
    kind: ProviderKind | None = None,
    current_user: User = Depends(get_current_user),
) -> list[ProviderRead]:
    # Reserved for policy checks in future phases.
    _ = current_user
    return [ProviderRead.model_validate(item, from_attributes=True) for item in list_provider_specs(kind)]


@router.post("/test", response_model=ProviderConnectionTestResponse)
async def test_connection(
    payload: ProviderConnectionTestRequest,
    current_user: User = Depends(get_current_user),
) -> ProviderConnectionTestResponse:
    _ = current_user
    result = probe_provider_connection(
        provider_slug=payload.provider_slug,
        endpoint=payload.endpoint,
        api_key=payload.api_key,
        model=payload.model,
    )
    return ProviderConnectionTestResponse(
        provider_slug=result.provider_slug,
        ok=result.ok,
        message=result.message,
        latency_ms=result.latency_ms,
        diagnostics=result.diagnostics,
    )


@router.post("/routing/preview", response_model=ProviderRoutingPreviewResponse)
async def routing_preview(
    payload: ProviderRoutingPreviewRequest,
    current_user: User = Depends(get_current_user),
) -> ProviderRoutingPreviewResponse:
    _ = current_user
    decision = route_for_task(payload.prompt, prefer_local=payload.prefer_local)
    return ProviderRoutingPreviewResponse(
        draft_provider=decision.draft_provider,
        refine_provider=decision.refine_provider,
        reason=decision.reason,
    )
