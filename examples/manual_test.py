
from agentblueprint_core import Agent, SequentialWorkflow
from agentblueprint_tools import CalculatorTool

def test_code_first():
    print("--- Testing Code-First API ---")
    
    agent = Agent(
        name="test_agent",
        model="mock:gpt-4",
        system_prompt="You are a test agent.",
        tools=[CalculatorTool()]
    )
    
    workflow = SequentialWorkflow(
        name="test_flow",
        agents=[agent]
    )
    
    result = workflow.run("Hello from code!")
    print(f"Result: {result}")

if __name__ == "__main__":
    test_code_first()
