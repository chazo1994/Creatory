from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class ProviderKind(str, enum.Enum):
    LLM = "llm"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    SEARCH = "search"
    SCRAPER = "scraper"


class ProviderMode(str, enum.Enum):
    CLOUD = "cloud"
    LOCAL = "local"


@dataclass(frozen=True)
class ProviderSpec:
    slug: str
    display_name: str
    kind: ProviderKind
    mode: ProviderMode
    default_model: str | None = None
    default_endpoint: str | None = None
    supports_streaming: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderConnectionResult:
    provider_slug: str
    ok: bool
    message: str
    latency_ms: int | None = None
    diagnostics: dict[str, Any] = field(default_factory=dict)
