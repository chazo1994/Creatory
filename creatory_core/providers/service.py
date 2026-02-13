from __future__ import annotations

import time
from urllib.parse import urlparse

from creatory_core.providers.base import (
    ProviderConnectionResult,
    ProviderKind,
    ProviderMode,
    ProviderSpec,
)
from creatory_core.providers.catalog import DEFAULT_PROVIDER_CATALOG


def list_provider_specs(kind: ProviderKind | None = None) -> list[ProviderSpec]:
    providers = list(DEFAULT_PROVIDER_CATALOG)
    if kind is None:
        return providers
    return [provider for provider in providers if provider.kind == kind]


def get_provider_spec_or_none(provider_slug: str) -> ProviderSpec | None:
    for provider in DEFAULT_PROVIDER_CATALOG:
        if provider.slug == provider_slug:
            return provider
    return None


def _looks_like_url(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def probe_provider_connection(
    provider_slug: str,
    endpoint: str | None,
    api_key: str | None,
    model: str | None,
) -> ProviderConnectionResult:
    started = time.perf_counter()
    spec = get_provider_spec_or_none(provider_slug)
    if spec is None:
        return ProviderConnectionResult(
            provider_slug=provider_slug,
            ok=False,
            message="Unknown provider slug",
        )

    resolved_endpoint = endpoint or spec.default_endpoint

    if spec.mode == ProviderMode.CLOUD and not api_key:
        return ProviderConnectionResult(
            provider_slug=provider_slug,
            ok=False,
            message="API key is required for cloud providers",
            diagnostics={"provider_mode": spec.mode.value},
        )

    if resolved_endpoint and not _looks_like_url(resolved_endpoint):
        return ProviderConnectionResult(
            provider_slug=provider_slug,
            ok=False,
            message="Endpoint must be a valid URL",
            diagnostics={"endpoint": resolved_endpoint},
        )

    latency_ms = int((time.perf_counter() - started) * 1000)
    response_message = "Connection profile validated (bootstrap runtime mock)."
    if spec.kind == ProviderKind.LLM and not (model or spec.default_model):
        response_message = "Connection validated, but no model is configured yet."

    return ProviderConnectionResult(
        provider_slug=provider_slug,
        ok=True,
        message=response_message,
        latency_ms=latency_ms,
        diagnostics={
            "provider_kind": spec.kind.value,
            "provider_mode": spec.mode.value,
            "resolved_model": model or spec.default_model,
            "resolved_endpoint": resolved_endpoint,
        },
    )
