"""
Validation script for loading ParallelWorkflow from config.
"""
import yaml
from pathlib import Path
from agentblueprint_config import load_and_parse
from agentblueprint_core import ParallelWorkflow

def test_config_parallel():
    print("\n🧪 Testing ParallelWorkflow Config Loading...")
    
    config_content = """
agents:
  a1:
    model: mock
    system_prompt: A1
  a2:
    model: mock
    system_prompt: A2

workflow:
  type: parallel
  agents:
    - a1
    - a2
"""
    # Write temp config
    p = Path("test_parallel.yaml")
    p.write_text(config_content)
    
    try:
        workflow = load_and_parse("test_parallel.yaml")
        
        assert isinstance(workflow, ParallelWorkflow)
        assert len(workflow.agents) == 2
        assert workflow.agents[0].name == "a1"
        assert workflow.agents[1].name == "a2"
        
        print("✅ Config loading successful")
        
        # Test Run
        results = workflow.run("Hello")
        assert "a1" in results
        assert "a2" in results
        print("✅ Execution from loaded workflow successful")
        
    finally:
        if p.exists():
            p.unlink()

if __name__ == "__main__":
    test_config_parallel()
