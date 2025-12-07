"""
Unit tests for AgentBlueprint Workflows.
"""
import pytest
from agentblueprint_core import (
    Agent, 
    SequentialWorkflow, 
    ParallelWorkflow, 
    GraphWorkflow, 
    WorkflowNode
)

@pytest.fixture
def mock_agent():
    return Agent(name="mock", model="mock", system_prompt="Sys")

@pytest.fixture
def echo_agent_a():
    return Agent(name="A", model="mock", system_prompt="A")

@pytest.fixture
def echo_agent_b():
    return Agent(name="B", model="mock", system_prompt="B")

def test_sequential_workflow(mock_agent):
    wf = SequentialWorkflow(
        name="seq_test",
        agents=[mock_agent, mock_agent]
    )
    # 1. Input -> Mock -> "ECHO: Input"
    # 2. "ECHO: Input" -> Mock -> "ECHO: ECHO: Input"
    result = wf.run("Input")
    assert "ECHO" in result
    assert "Input" in result

def test_parallel_workflow(echo_agent_a, echo_agent_b):
    wf = ParallelWorkflow(
        name="par_test",
        agents=[echo_agent_a, echo_agent_b]
    )
    results = wf.run("Start")
    assert results["A"] == "ECHO (A): Start"
    assert results["B"] == "ECHO (B): Start"

def test_graph_workflow(echo_agent_a, echo_agent_b):
    # A -> B
    nodes = [
        WorkflowNode(id="node_a", agent=echo_agent_a, depends_on=[]),
        WorkflowNode(id="node_b", agent=echo_agent_b, depends_on=["node_a"]),
    ]
    wf = GraphWorkflow(
        name="graph_test",
        nodes=nodes
    )
    results = wf.run("Start")
    
    # A output
    assert results["node_a"] == "ECHO (A): Start"
    
    # B output should contain A's output
    assert "ECHO (A): Start" in results["node_b"]
