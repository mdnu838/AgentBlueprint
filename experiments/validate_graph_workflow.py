"""
Validation script for GraphWorkflow.
"""
from agentblueprint_core import Agent, GraphWorkflow, WorkflowNode
from agentblueprint_tools import EchoTool

def test_graph_execution():
    print("\n🧪 Testing GraphWorkflow...")
    
    # Define agents
    agent_a = Agent(name="A", model="mock", system_prompt="A", tools=[])
    agent_b = Agent(name="B", model="mock", system_prompt="B", tools=[])
    agent_c = Agent(name="C", model="mock", system_prompt="C", tools=[])
    
    # Graph:
    # A -> B
    # A -> C
    # B, C -> (implicit result collection) - Wait, we just depend on execution.
    # Let's add a joiner node D.
    agent_d = Agent(name="D", model="mock", system_prompt="D", tools=[])

    # A runs with initial input
    # B runs after A (receives A's output)
    # C runs after A (receives A's output)
    # D runs after B and C (receives B and C's output)
    
    nodes = [
        WorkflowNode(id="node_a", agent=agent_a, depends_on=[]),
        WorkflowNode(id="node_b", agent=agent_b, depends_on=["node_a"]),
        WorkflowNode(id="node_c", agent=agent_c, depends_on=["node_a"]),
        WorkflowNode(id="node_d", agent=agent_d, depends_on=["node_b", "node_c"]),
    ]
    
    workflow = GraphWorkflow(
        name="graph_test",
        nodes=nodes
    )
    
    input_text = "Start"
    results = workflow.run(input_text)
    
    print(f"Results: {results}")
    
    # Verify execution order via dependencies (implicit in the fact they ran)
    # A output should contain "Start"
    assert "Start" in results["node_a"]
    
    # B and C should contain A's output
    # B and C should contain A's output
    # Since agent_a is "echo", its output is "ECHO (A): Start"
    assert "ECHO (A): Start" in results["node_b"]
    assert "ECHO (A): Start" in results["node_c"]
    
    # D should contain B and C's output
    assert "Output from node_b" in results["node_d"]
    assert "Output from node_c" in results["node_d"]
    
    print("✅ Graph execution successful")

if __name__ == "__main__":
    test_graph_execution()
