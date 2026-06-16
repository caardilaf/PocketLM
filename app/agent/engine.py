from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Protocol, TypedDict

from langgraph.graph import END, StateGraph

from app.agent.schemas import AgentResult, TaskType


class ModelClient(Protocol):
    async def generate(self, prompt: str) -> str: ...


class EchoModelClient:
    async def generate(self, prompt: str) -> str:
        return prompt


class AgentState(TypedDict, total=False):
    task_type: TaskType
    text: str
    prompt: str
    raw_output: str
    output: str
    metadata: dict[str, Any]


@dataclass
class AgentEngine:
    model_client: ModelClient

    def __post_init__(self) -> None:
        self._graph = self._build_graph().compile()

    async def run(self, task_type: TaskType, text: str) -> AgentResult:
        state = await self._graph.ainvoke({"task_type": task_type, "text": text, "metadata": {}})
        return AgentResult(
            task_type=task_type,
            output=state["output"],
            metadata={**state.get("metadata", {}), "provider": "model-agnostic", "engine": "langgraph"},
        )

    def _build_graph(self) -> StateGraph[AgentState]:
        graph = StateGraph(AgentState)
        graph.add_node("build_prompt", self._build_prompt)
        graph.add_node("call_model", self._call_model)
        graph.add_node("postprocess", self._postprocess)
        graph.set_entry_point("build_prompt")
        graph.add_edge("build_prompt", "call_model")
        graph.add_edge("call_model", "postprocess")
        graph.add_edge("postprocess", END)
        return graph

    async def _build_prompt(self, state: AgentState) -> AgentState:
        task_type = state["task_type"]
        text = state["text"]
        if task_type is TaskType.classification:
            prompt = f"Classify this text into a concise category: {text}"
        else:
            prompt = f"Summarize this text in one short paragraph: {text}"
        return {**state, "prompt": prompt}

    async def _call_model(self, state: AgentState) -> AgentState:
        raw_output = await self.model_client.generate(state["prompt"])
        return {**state, "raw_output": raw_output}

    async def _postprocess(self, state: AgentState) -> AgentState:
        task_type = state["task_type"]
        raw_output = state.get("raw_output", "").strip()
        text = state["text"]
        output = raw_output or (
            _fallback_classification(text) if task_type is TaskType.classification else _fallback_summary(text)
        )
        metadata = dict(state.get("metadata", {}))
        metadata["fallback_used"] = not bool(raw_output)
        return {**state, "output": output, "metadata": metadata}


_KEYWORDS = {
    "billing": "billing",
    "invoice": "billing",
    "payment": "billing",
    "bug": "support",
    "error": "support",
    "refund": "support",
    "summary": "general",
}


def _fallback_classification(text: str) -> str:
    lowered = text.lower()
    for keyword, label in _KEYWORDS.items():
        if keyword in lowered:
            return label
    return "general"


def _fallback_summary(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= 140:
        return text
    return text[:137].rstrip() + "..."
