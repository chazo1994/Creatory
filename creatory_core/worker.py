from __future__ import annotations

import asyncio
import logging

from creatory_core.core.config import settings

logger = logging.getLogger("creatory.worker")


async def run_forever() -> None:
    logger.info("agent orchestrator worker started", extra={"redis_url": settings.redis_url})
    while True:
        # Placeholder heartbeat loop for future queue-based orchestration.
        await asyncio.sleep(15)
        logger.info("worker heartbeat")


def main() -> None:
    logging.basicConfig(level=settings.log_level.upper())
    asyncio.run(run_forever())


if __name__ == "__main__":
    main()
