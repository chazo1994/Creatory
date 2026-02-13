import asyncio

from creatory_core.api.routes.health import live
from creatory_core.main import root


def test_root_status() -> None:
    payload = asyncio.run(root())
    assert payload["status"] == "ok"


def test_live_probe() -> None:
    assert asyncio.run(live()) == {"status": "ok"}
