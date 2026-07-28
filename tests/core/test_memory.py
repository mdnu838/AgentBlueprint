import pytest
from agentblueprint_core.memory import SimpleMemory, NoOpMemory

def test_simple_memory_get_context():
    memory = SimpleMemory()

    # Test empty memory
    assert memory.get_context() == ""
    assert memory.get_history() == []

    # Add messages
    memory.add("user", "Hello, assistant!")
    memory.add("assistant", "Hello, user! How can I help you today?")
    memory.add("user", "I have a question about Python.")

    # Test history
    history = memory.get_history()
    assert len(history) == 3
    assert history[0] == {"role": "user", "content": "Hello, assistant!"}
    assert history[1] == {"role": "assistant", "content": "Hello, user! How can I help you today?"}
    assert history[2] == {"role": "user", "content": "I have a question about Python."}

    # Test context
    context = memory.get_context()
    expected_context = (
        "USER: Hello, assistant!\n"
        "ASSISTANT: Hello, user! How can I help you today?\n"
        "USER: I have a question about Python."
    )
    assert context == expected_context

def test_no_op_memory():
    memory = NoOpMemory()

    # Test empty memory
    assert memory.get_context() == ""
    assert memory.get_history() == []

    # Add messages
    memory.add("user", "Hello, assistant!")
    memory.add("assistant", "Hello, user! How can I help you today?")

    # Test history is still empty
    assert memory.get_history() == []

    # Test context is still empty string
    assert memory.get_context() == ""
