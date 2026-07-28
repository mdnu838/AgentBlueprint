import pytest
from agentblueprint_core.memory import SQLMemory, SimpleMemory
from agentblueprint_core.state import SQLWorkflowStateStore

def test_simple_memory():
    memory = SimpleMemory()

    # Check initial state
    assert len(memory.get_history()) == 0

    # Add messages
    memory.add("user", "Hello")
    memory.add("assistant", "Hi there!")

    # Check history
    history = memory.get_history()
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "Hello"}
    assert history[1] == {"role": "assistant", "content": "Hi there!"}

def test_sql_memory():
    memory = SQLMemory(db_url="sqlite:///:memory:", session_id="test_session")

    # Add messages
    memory.add("user", "Hello")
    memory.add("assistant", "Hi there!")

    # Check history
    history = memory.get_history()
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "Hello"}
    assert history[1] == {"role": "assistant", "content": "Hi there!"}

    # Check context
    context = memory.get_context()
    assert "USER: Hello" in context
    assert "ASSISTANT: Hi there!" in context

    # Test session isolation
    memory2 = SQLMemory(db_url=memory.db_url, session_id="another_session")

    assert len(memory2.get_history()) == 0
    memory2.add("user", "Testing isolation")
    assert len(memory2.get_history()) == 1
    assert len(memory.get_history()) == 2

def test_sql_workflow_state_store():
    store = SQLWorkflowStateStore(db_url="sqlite:///:memory:")

    # Test load non-existent
    state = store.load_state("wf_1")
    assert state == {}

    # Test save and load
    store.save_state("wf_1", {"status": "running", "step": 1})
    state = store.load_state("wf_1")
    assert state == {"status": "running", "step": 1}

    # Test update
    store.save_state("wf_1", {"status": "completed", "step": 2, "result": "done"})
    state = store.load_state("wf_1")
    assert state == {"status": "completed", "step": 2, "result": "done"}

    # Test multiple workflows
    store.save_state("wf_2", {"status": "pending"})
    assert store.load_state("wf_2") == {"status": "pending"}
    assert store.load_state("wf_1") == {"status": "completed", "step": 2, "result": "done"}
