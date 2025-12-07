"""
Validation script for Observability (Callbacks).
"""
from agentblueprint_core import Agent, SequentialWorkflow, CallbackHandler
from typing import Any

class TestCallback(CallbackHandler):
    def __init__(self):
        self.events = []
        
    def on_agent_start(self, name: str, input_text: str) -> None:
        self.events.append(f"start:{name}")
        
    def on_agent_end(self, name: str, response: str) -> None:
        self.events.append(f"end:{name}")

def test_observability():
    print("\n🧪 Testing Observability...")
    
    agent = Agent(name="test_obs", model="mock", system_prompt="Test")
    callback = TestCallback()
    
    # 1. Test direct agent run
    print("Run Agent with callback...")
    agent.run("Input", callbacks=[callback])
    
    print(f"Events: {callback.events}")
    assert "start:test_obs" in callback.events
    assert "end:test_obs" in callback.events
    
    # 2. Test workflow propagation
    print("Run Workflow with callback...")
    callback.events = [] # reset
    wf = SequentialWorkflow(name="seq", agents=[agent])
    wf.run("Input", callbacks=[callback])
    
    print(f"Events: {callback.events}")
    assert "start:test_obs" in callback.events
    assert "end:test_obs" in callback.events
    
    print("✅ Observability validation successful")

if __name__ == "__main__":
    test_observability()
