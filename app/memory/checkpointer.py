from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryCheckpointer:
    """Simple in-memory store for conversation checkpoints."""
    _store: dict[str, dict[str, Any]] = field(default_factory=dict)

    def get(self, conversation_id: str) -> dict[str, Any] | None:
        """Fetch a copy of the stored state for a conversation."""
        state = self._store.get(conversation_id)
        return None if state is None else dict(state)

    def set(self, conversation_id: str, state: dict[str, Any]) -> None:
        """Store a copy of the state for a conversation."""
        self._store[conversation_id] = dict(state)
