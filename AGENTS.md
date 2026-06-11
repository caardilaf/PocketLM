# PocketLM — Agent Guide

## Commands

```sh
uv run python main.py    # run entrypoint
uv sync                  # sync deps from pyproject.toml + uv.lock
uv add <package>         # add a dependency
```

## Package manager

Use **uv** (not pip). The `.venv/` was created by `uv venv`. `uv.lock` is committed.

## Python

- **Python 3.13+** required (`requires-python`, `.python-version`).
- No dependencies declared yet (`dependencies = []`).
- No test framework, linter, or formatter configured. Add config under `[tool.*]` in `pyproject.toml` before running any.

## Entrypoint

- `main.py:55` — `main()` called under `if __name__ == "__main__"`.
- Currently contains a `fibonacci(n, use_cache)` memoization demo.

## Project state

Early skeleton. No CI, no tests, minimal structure. All substantive work is still to be done.
