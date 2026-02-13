from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class MCPRegistryLoadError(ValueError):
    """Raised when MCP registry manifest cannot be loaded."""


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def registry_manifest_path() -> Path:
    return _project_root() / "mcp" / "registry" / "default_manifest.yaml"


def load_registry_manifest() -> dict[str, Any]:
    manifest_path = registry_manifest_path()
    if not manifest_path.exists():
        raise MCPRegistryLoadError("Registry manifest file is missing")

    loaded = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise MCPRegistryLoadError("Registry manifest root must be a mapping")
    return loaded
