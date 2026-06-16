# PocketLM API — Post-Review Spec Update

**Date:** 2026-06-15  
**Version:** 20260615-review

## 1. Purpose
Refine the PocketLM API implementation after code review. The goal is to improve correctness, clarity, and testability while keeping the project lightweight and model-agnostic.

## 2. Review-Driven Goals
- Clarify configuration semantics.
- Improve concurrency/rate-limit handling.
- Strengthen HTTP error mapping and endpoint behavior.
- Tighten validation and edge-case handling.
- Increase test coverage for failure paths.
- Keep LangGraph integration small but explicit.

## 3. Current Implementation Notes
- FastAPI app exists with `/health`, `/version`, and `/agent/run`.
- LangGraph is used for a minimal agent pipeline.
- In-memory checkpointing is implemented.
- Validation exists for blank text and memory usage without conversation ID.
- Rate-limit and validation exceptions are mapped to HTTP responses.

## 4. Issues to Address
### Code quality
- Remove unused imports and unnecessary complexity.
- Make limiter behavior more explicit and less fragile.
- Use names that match behavior for config settings.

### Error handling
- Ensure 429 responses are tested end-to-end.
- Ensure 422 responses are consistent for both request validation and service validation.
- Improve handling of malformed or empty model outputs.

### Edge cases
- Empty/whitespace input text.
- Missing conversation IDs when memory is enabled.
- Missing previous state in checkpoint store.
- Rate limit overflow / contention.
- Model returns blank output.

### Testing
- Add/keep tests for:
  - HTTP success and failure responses.
  - Memory isolation between conversations.
  - Rate limit behavior.
  - Fallback output behavior.
  - Validation errors.

## 5. Refined Architecture Constraints
- Keep FastAPI as the HTTP layer.
- Keep LangGraph as the task orchestration layer.
- Keep model abstraction provider-agnostic.
- Keep short-term memory in-process only.
- Avoid introducing heavyweight infrastructure.

## 6. Configuration Plan
- `app_name` and `version` stay shared across app and endpoints.
- Concurrency limit should clearly represent concurrency, not request timeout.
- If a timeout is needed, distinguish it from request queue/acquire behavior.

## 7. Acceptance Criteria
- Tests pass.
- Version is sourced from shared config.
- Rate-limit failures return HTTP 429.
- Memory validation failures return HTTP 422.
- No brittle use of semaphore internals.
- Agent flow remains minimal and readable.

## 8. Next Step
Use this update as the baseline for any follow-up implementation cleanup, then re-run the full test suite.
