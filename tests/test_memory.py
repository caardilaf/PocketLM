from app.memory.checkpointer import InMemoryCheckpointer


def test_checkpointer_copies_data():
    cp = InMemoryCheckpointer()
    state = {"a": 1}
    cp.set("x", state)
    state["a"] = 2
    assert cp.get("x") == {"a": 1}


def test_missing_state_returns_none():
    cp = InMemoryCheckpointer()
    assert cp.get("missing") is None
