from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


client = TestClient(create_app())


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == get_settings().version


def test_classification_route():
    response = client.post(
        "/agent/run",
        json={"task_type": "classification", "text": "Invoice payment failed", "use_memory": False},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["task_type"] == "classification"
    assert body["output"]


def test_summarization_route():
    response = client.post(
        "/agent/run",
        json={"task_type": "summarization", "text": "PocketLM is a small API for agent tasks.", "use_memory": False},
    )
    assert response.status_code == 200
    assert response.json()["task_type"] == "summarization"


def test_validation_error_when_memory_without_conversation_id():
    response = client.post(
        "/agent/run",
        json={"task_type": "classification", "text": "hello", "use_memory": True},
    )
    assert response.status_code == 422


def test_invalid_payload_rejected():
    response = client.post("/agent/run", json={"task_type": "classification", "text": "   "})
    assert response.status_code == 422


def test_rate_limit_maps_to_429():
    import asyncio

    from app.agent.engine import AgentEngine
    from app.core.dependencies import get_agent_service
    from app.services.agent_service import AgentService

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
