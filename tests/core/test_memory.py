import pytest
from agentblueprint_core.memory import NoOpMemory

def test_noop_memory_get_context():
    memory = NoOpMemory()
    assert memory.get_context() == ""
