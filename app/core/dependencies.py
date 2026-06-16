from __future__ import annotations

import asyncio

from app.agent.engine import AgentEngine, EchoModelClient
from app.core.config import get_settings
from app.services.agent_service import AgentService

_service: AgentService | None = None


def get_agent_service() -> AgentService:
    global _service
    if _service is None:
        settings = get_settings()
        _service = AgentService(
            engine=AgentEngine(model_client=EchoModelClient()),
            semaphore=asyncio.Semaphore(settings.max_concurrent_requests),
            acquire_timeout_seconds=settings.acquire_timeout_seconds,
        )
    return _service
