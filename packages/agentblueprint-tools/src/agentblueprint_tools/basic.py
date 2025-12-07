"""
Basic tools for AgentBlueprint.
"""
from agentblueprint_core import Tool

class CalculatorTool(Tool):
    """
    A simple calculator tool.
    """
    name = "calculator"
    description = "Performs basic mathematical calculations. Input should be a valid python expression string."
    
    def run(self, expression: str) -> str:
        try:
            # WARNING: eval is unsafe in production, but okay for this proof-of-concept/testing tool
            return str(eval(expression))
        except Exception as e:
            return f"Error: {str(e)}"

class EchoTool(Tool):
    """
    A tool that echoes the input.
    """
    name = "echo"
    description = "Echoes back the input."
    
    def run(self, text: str) -> str:
        return f"Echo: {text}"
