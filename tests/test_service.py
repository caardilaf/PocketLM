import asyncio

import pytest

from app.agent.engine import AgentEngine
from app.agent.schemas import AgentRunRequest, TaskType
from app.core.errors import RateLimitError, TaskValidationError
from app.memory.checkpointer import InMemoryCheckpointer
from app.services.agent_service import AgentService


class StubModel:
    async def generate(self, prompt: str) -> str:
        return "ok"


def test_memory_roundtrip():
    service = AgentService(
        engine=AgentEngine(model_client=StubModel()),
        checkpointer=InMemoryCheckpointer(),
        semaphore=asyncio.Semaphore(1),
    )
    request = AgentRunRequest(task_type=TaskType.classification, text="hello", use_memory=True, conversation_id="abc")
    first = asyncio.run(service.run(request))
    second = asyncio.run(service.run(request))
    assert first.conversation_id == "abc"
    assert second.metadata["previous_state"]["last_output"] == "ok"


def test_memory_isolated_between_conversations():
    service = AgentService(
        engine=AgentEngine(model_client=StubModel()),
        checkpointer=InMemoryCheckpointer(),
        semaphore=asyncio.Semaphore(2),
    )
    first = asyncio.run(service.run(AgentRunRequest(task_type=TaskType.classification, text="hello", use_memory=True, conversation_id="a")))
    second = asyncio.run(service.run(AgentRunRequest(task_type=TaskType.classification, text="hello", use_memory=True, conversation_id="b")))
    assert first.conversation_id == "a"
    assert "previous_state" not in second.metadata


def test_missing_conversation_id_with_memory_raises_validation_error():
    service = AgentService(engine=AgentEngine(model_client=StubModel()))
    with pytest.raises(TaskValidationError):
        asyncio.run(service.run(AgentRunRequest(task_type=TaskType.classification, text="hello", use_memory=True)))


def test_rate_limit_overflow_raises():
    service = AgentService(
        engine=AgentEngine(model_client=StubModel()),
        semaphore=asyncio.Semaphore(0),
        acquire_timeout_seconds=0.01,
    )
    with pytest.raises(RateLimitError):
        asyncio.run(service.run(AgentRunRequest(task_type=TaskType.classification, text="hello")))
