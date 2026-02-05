from app.db.models import ThreadKind
from app.services.director import _assistant_text, _build_plan


def test_build_plan_for_main_thread() -> None:
    plan = _build_plan("Create a TikTok launch script", ThreadKind.MAIN)
    assert len(plan) >= 4
    assert any("tool" in step.lower() for step in plan)


def test_build_plan_for_quick_thread() -> None:
    plan = _build_plan("Need 3 hook ideas", ThreadKind.QUICK)
    assert len(plan) == 2


def test_assistant_text_quick_contains_recommendation() -> None:
    text = _assistant_text("Need punchy CTA", ThreadKind.QUICK, ["step"])
    assert "Recommendation" in text


def test_assistant_text_main_contains_execution_plan() -> None:
    text = _assistant_text("Create launch plan", ThreadKind.MAIN, ["a", "b"])
    assert "Execution plan" in text
