from agentblueprint_core.memory import NoOpMemory

def test_noop_memory():
    memory = NoOpMemory()

    # Check initial history
    assert memory.get_history() == []

    # Add a message
    memory.add(role="user", content="test message")

    # Check history is still empty
    assert memory.get_history() == []
