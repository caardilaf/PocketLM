# PocketLM — Agent Guide

## Quick start

```sh
python main.py
```

## Python

- **Python 3.13+** required (`pyproject.toml` `requires-python`, `.python-version`).
- No dependencies declared yet (`dependencies = []`).
- No test framework, linter, or formatter configured. Add config to `pyproject.tool` before running any.

## Entrypoint

- `main.py` — module-level `main()` called under `if __name__ == "__main__"`.

## Project state

Early skeleton. No CI, no tests, minimal structure. All substantive work is still to be done.
