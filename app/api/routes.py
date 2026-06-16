from __future__ import annotations

from fastapi import APIRouter, Depends

from app.agent.schemas import AgentResult, AgentRunRequest
from app.core.config import get_settings
from app.core.dependencies import get_agent_service
from app.services.agent_service import AgentService

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """Return a simple health status payload."""
    return {"status": "ok"}


@router.get("/version")
async def version() -> dict[str, str]:
    """Return the application version from shared settings."""
    return {"version": get_settings().version}


@router.post("/agent/run", response_model=AgentResult)
async def run_agent(
    request: AgentRunRequest,
    service: AgentService = Depends(get_agent_service),
) -> AgentResult:
    """Run a single agent task using the configured service."""
    return await service.run(request)
