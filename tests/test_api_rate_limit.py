import asyncio

from fastapi.testclient import TestClient

from app.agent.engine import AgentEngine
from app.core.dependencies import get_agent_service
from app.main import create_app
from app.services.agent_service import AgentService


client = TestClient(create_app())


def test_rate_limit_maps_to_429():
    class SlowModel:
        async def generate(self, prompt: str) -> str:
            return "ok"

    service = AgentService(
        engine=AgentEngine(model_client=SlowModel()),
        semaphore=asyncio.Semaphore(0),
        acquire_timeout_seconds=0.01,
    )
    app = client.app
    app.dependency_overrides[get_agent_service] = lambda: service
    try:
        response = client.post(
            "/agent/run",
            json={"task_type": "classification", "text": "hello", "use_memory": False},
        )
        assert response.status_code == 429
    finally:
        app.dependency_overrides.clear()
