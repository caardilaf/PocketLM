from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryCheckpointer:
    _store: dict[str, dict[str, Any]] = field(default_factory=dict)

    def get(self, conversation_id: str) -> dict[str, Any] | None:
        state = self._store.get(conversation_id)
        return None if state is None else dict(state)

    def set(self, conversation_id: str, state: dict[str, Any]) -> None:
        self._store[conversation_id] = dict(state)
