from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from app.agent.engine import AgentEngine
from app.agent.schemas import AgentResult, AgentRunRequest
from app.core.errors import RateLimitError, TaskValidationError
from app.memory.checkpointer import InMemoryCheckpointer


@dataclass
class AgentService:
    engine: AgentEngine
    checkpointer: InMemoryCheckpointer = field(default_factory=InMemoryCheckpointer)
    semaphore: asyncio.Semaphore = field(default_factory=lambda: asyncio.Semaphore(4))
    acquire_timeout_seconds: float = 0.0

    async def run(self, request: AgentRunRequest) -> AgentResult:
        if request.use_memory and not request.conversation_id:
            raise TaskValidationError("conversation_id is required when use_memory is enabled")

        acquired = await self._acquire_slot()
        if not acquired:
            raise RateLimitError("Too many concurrent requests")

        try:
            previous_state = None
            if request.use_memory and request.conversation_id:
                previous_state = self.checkpointer.get(request.conversation_id)

            result = await self.engine.run(request.task_type, request.text)
            metadata = dict(result.metadata)
            if previous_state is not None:
                metadata["previous_state"] = previous_state

            final_result = result.model_copy(update={"metadata": metadata, "conversation_id": request.conversation_id})
            if request.use_memory and request.conversation_id:
                self.checkpointer.set(
                    request.conversation_id,
                    {"task_type": request.task_type.value, "last_output": final_result.output},
                )
            return final_result
        finally:
            self.semaphore.release()

    async def _acquire_slot(self) -> bool:
        try:
            if self.acquire_timeout_seconds > 0:
                await asyncio.wait_for(self.semaphore.acquire(), timeout=self.acquire_timeout_seconds)
            else:
                await self.semaphore.acquire()
            return True
        except TimeoutError:
            return False
