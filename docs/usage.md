# PocketLM Usage

## Run the API

```sh
uv run python main.py
```

## Endpoints

- `GET /health` — health check
- `GET /version` — version info
- `POST /agent/run` — run a classification or summarization task

## Example request

```json
{
  "task_type": "classification",
  "text": "Invoice payment failed",
  "use_memory": false
}
```

## Notes

- The service is model-agnostic.
- Short-term memory is in-process only.
- If `use_memory` is true, `conversation_id` is required.
- Rate limiting is enforced with a semaphore-based concurrency guard.
