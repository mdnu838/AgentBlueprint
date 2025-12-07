"""
Validation script for loading GraphWorkflow from config.
"""
from pathlib import Path
from agentblueprint_config import load_and_parse
from agentblueprint_core import GraphWorkflow

def test_config_graph():
    print("\n🧪 Testing GraphWorkflow Config Loading...")
    
    config_content = """
agents:
  a1:
    model: mock
    system_prompt: A1
  a2:
    model: mock
    system_prompt: A2

workflow:
  type: graph
  nodes:
    - id: step_1
      agent: a1
    - id: step_2
      agent: a2
      depends_on: [step_1]
"""
    # Write temp config
    p = Path("test_graph.yaml")
    p.write_text(config_content)
    
    try:
        workflow = load_and_parse("test_graph.yaml")
        
        assert isinstance(workflow, GraphWorkflow)
        assert len(workflow.nodes) == 2
        
        # Verify wiring
        node_map = {node.id: node for node in workflow.nodes}
        assert "step_1" in node_map
        assert "step_2" in node_map
        assert node_map["step_2"].depends_on == ["step_1"]
        
        print("✅ Config loading successful")
        
        # Test Run
        results = workflow.run("Graph Start")
        assert "step_1" in results
        assert "step_2" in results
        # Validation of flow content
        assert "Graph Start" in results["step_1"]
        assert "Output from step_1" in results["step_2"]
        
        print(f"Result 2: {results['step_2']}")
        print("✅ Execution from loaded workflow successful")
        
    finally:
        if p.exists():
            p.unlink()

if __name__ == "__main__":
    test_config_graph()
