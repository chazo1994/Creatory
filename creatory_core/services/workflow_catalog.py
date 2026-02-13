from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class WorkflowTemplateLoadError(ValueError):
    """Raised when a workflow template file cannot be parsed."""


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def templates_dir() -> Path:
    return _project_root() / "workflows" / "templates"


def load_template_file(filename: str) -> dict[str, Any]:
    path = templates_dir() / filename
    if not path.exists():
        raise WorkflowTemplateLoadError(f"Template file not found: {filename}")

    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - defensive loader
        raise WorkflowTemplateLoadError(f"Invalid YAML in template: {filename}") from exc

    if not isinstance(loaded, dict):
        raise WorkflowTemplateLoadError(f"Template root must be an object: {filename}")

    return loaded
