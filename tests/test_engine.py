import asyncio

from app.agent.engine import AgentEngine
from app.agent.schemas import TaskType


class StubModel:
    def __init__(self, response: str):
        self.response = response
        self.prompts: list[str] = []

    async def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


def test_classification_uses_model():
    model = StubModel("support")
    engine = AgentEngine(model_client=model)
    result = asyncio.run(engine.run(TaskType.classification, "payment failed"))
    assert result.output == "support"
    assert "Classify" in model.prompts[0]
    assert result.metadata["engine"] == "langgraph"


def test_summarization_uses_model():
    model = StubModel("short summary")
    engine = AgentEngine(model_client=model)
    result = asyncio.run(engine.run(TaskType.summarization, "Lots of text"))
    assert result.output == "short summary"


def test_fallback_classification():
    engine = AgentEngine(model_client=StubModel(""))
    result = asyncio.run(engine.run(TaskType.classification, "Refund request about invoice"))
    assert result.output == "billing"


def test_fallback_classification_general_case():
    engine = AgentEngine(model_client=StubModel(""))
    result = asyncio.run(engine.run(TaskType.classification, "hello world"))
    assert result.output == "general"


def test_fallback_summary_truncates_long_text():
    engine = AgentEngine(model_client=StubModel(""))
    result = asyncio.run(engine.run(TaskType.summarization, "x " * 200))
    assert result.output.endswith("...")
