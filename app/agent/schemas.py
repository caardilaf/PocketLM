from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class TaskType(str, Enum):
    classification = "classification"
    summarization = "summarization"


class AgentRunRequest(BaseModel):
    task_type: TaskType
    text: str = Field(min_length=1)
    conversation_id: str | None = None
    use_memory: bool = False

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must not be blank")
        return value


class AgentResult(BaseModel):
    task_type: TaskType
    output: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    conversation_id: str | None = None
