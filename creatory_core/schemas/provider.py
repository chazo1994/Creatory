from pydantic import BaseModel, Field

from creatory_core.providers.base import ProviderKind, ProviderMode


class ProviderRead(BaseModel):
    slug: str
    display_name: str
    kind: ProviderKind
    mode: ProviderMode
    default_model: str | None = None
    default_endpoint: str | None = None
    supports_streaming: bool = False
    metadata: dict = Field(default_factory=dict)


class ProviderConnectionTestRequest(BaseModel):
    provider_slug: str
    endpoint: str | None = None
    api_key: str | None = None
    model: str | None = None


class ProviderConnectionTestResponse(BaseModel):
    provider_slug: str
    ok: bool
    message: str
    latency_ms: int | None = None
    diagnostics: dict = Field(default_factory=dict)


class ProviderRoutingPreviewRequest(BaseModel):
    prompt: str
    prefer_local: bool = False


class ProviderRoutingPreviewResponse(BaseModel):
    draft_provider: str
    refine_provider: str
    reason: str
