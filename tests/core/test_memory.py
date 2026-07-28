import pytest
from agentblueprint_core.memory import NoOpMemory

def test_noop_memory():
    memory = NoOpMemory()

    # Test adding a message doesn't raise exception
    memory.add("user", "Hello")

    # Check history is always empty
    history = memory.get_history()
    assert history == []

    # Check context is always empty
    context = memory.get_context()
    assert context == ""
