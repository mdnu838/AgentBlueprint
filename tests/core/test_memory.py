from agentblueprint_core.memory import NoOpMemory

def test_noop_memory_get_history():
    """Test that NoOpMemory.get_history always returns an empty list."""
    memory = NoOpMemory()

    # Check initial state
    assert memory.get_history() == []

    # Check state after attempting to add an item
    memory.add(role="user", content="hello")
    assert memory.get_history() == []
