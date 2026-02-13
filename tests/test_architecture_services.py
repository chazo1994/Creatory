from types import SimpleNamespace
from uuid import uuid4

import pytest

from creatory_core.providers.service import list_provider_specs, probe_provider_connection
from creatory_core.services.bridge import normalize_context_block
from creatory_core.services.circuit_breaker import (
    CircuitBreakerConfig,
    CircuitBreakerTriggered,
    assert_step_budget,
)


def test_provider_catalog_contains_llm_and_media_options() -> None:
    providers = list_provider_specs()
    slugs = {provider.slug for provider in providers}
    assert "openai" in slugs
    assert "ollama" in slugs
    assert "flux" in slugs


def test_provider_connection_requires_api_key_for_cloud() -> None:
    result = probe_provider_connection(
        provider_slug="openai",
        endpoint="https://api.openai.com/v1",
        api_key=None,
        model="gpt-4.1-mini",
    )
    assert result.ok is False
    assert "API key" in result.message


def test_bridge_normalize_uses_message_text_when_payload_missing() -> None:
    source_message = SimpleNamespace(
        id=uuid4(),
        content_json={"text": "Quick insight from side chat"},
    )
    block = normalize_context_block(source_message, payload_block={})
    assert block["text"] == "Quick insight from side chat"
    assert block["source"] == "quick-thread"


def test_circuit_breaker_raises_when_exceeding_step_limit() -> None:
    with pytest.raises(CircuitBreakerTriggered):
        assert_step_budget(requested_steps=16, config=CircuitBreakerConfig(max_steps=15))
