from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CircuitBreakerConfig:
    max_steps: int = 15


class CircuitBreakerTriggered(RuntimeError):
    """Raised when orchestration exceeds safety budgets."""


def assert_step_budget(*, requested_steps: int, config: CircuitBreakerConfig) -> None:
    if requested_steps <= config.max_steps:
        return
    raise CircuitBreakerTriggered(
        f"Circuit breaker triggered: requested_steps={requested_steps} exceeds "
        f"max_steps={config.max_steps}"
    )
