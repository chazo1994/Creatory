from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderRoutingDecision:
    draft_provider: str
    refine_provider: str
    reason: str


def route_for_task(prompt: str, prefer_local: bool = False) -> ProviderRoutingDecision:
    normalized_prompt = prompt.lower().strip()
    complex_markers = (
        "strategy",
        "campaign",
        "go-to-market",
        "research",
        "multi-step",
        "long-form",
    )
    is_complex = any(marker in normalized_prompt for marker in complex_markers)

    if prefer_local:
        return ProviderRoutingDecision(
            draft_provider="ollama",
            refine_provider="vllm" if is_complex else "ollama",
            reason="Local-first routing requested by workspace or user preference.",
        )

    if is_complex:
        return ProviderRoutingDecision(
            draft_provider="ollama",
            refine_provider="openai",
            reason="Complex request detected: use low-cost draft + higher-reasoning refinement.",
        )

    return ProviderRoutingDecision(
        draft_provider="ollama",
        refine_provider="openai",
        reason="Default hybrid route for responsive drafting and reliable final polish.",
    )
