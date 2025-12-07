"""
Validation script for ParallelWorkflow.
"""
from agentblueprint_core import Agent, ParallelWorkflow
from agentblueprint_tools import EchoTool
import time

def test_parallel_execution():
    print("\n🧪 Testing ParallelWorkflow...")
    
    # Define agents
    agent1 = Agent(name="agent1", model="mock", system_prompt="Sys", tools=[])
    agent2 = Agent(name="agent2", model="mock", system_prompt="Sys", tools=[])
    
    # Using a Mock or just standard Agent run (which is fast)
    # To truly test parallel we might want a slow tool, but for basic logic check:
    
    workflow = ParallelWorkflow(
        name="parallel_test",
        agents=[agent1, agent2]
    )
    
    input_text = "Test Input"
    print(f"Input: {input_text}")
    
    results = workflow.run(input_text)
    
    print(f"Results: {results}")
    
    assert "agent1" in results
    assert "agent2" in results
    # Check that they both ran
    assert "ECHO" in results["agent1"]
    assert "ECHO" in results["agent2"]
    
    print("✅ Parallel execution successful")

if __name__ == "__main__":
    test_parallel_execution()
