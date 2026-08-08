"""
Python REPL tool for executing code.
"""
import sys
import subprocess
from typing import Optional
from agentblueprint_core import Tool

class PythonREPLTool(Tool):
    """
    A tool for running Python code.
    Executes code locally in an isolated subprocess without passing environment variables.
    WARNING: This is safer than eval/exec but not fully sandboxed. Use with caution.
    """
    name = "python_repl"
    description = "Executes Python code and returns stdout/stderr. Input should be valid python code."
    
    def run(self, code: str) -> str:
        """Execute the python code in a subprocess and return the output."""
        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=10,
                env={}  # Clear environment to avoid leaking secrets
            )
            
            output = result.stdout
            if result.stderr:
                output += "\n" + result.stderr if output else result.stderr

            if not output.strip() and result.returncode == 0:
                return "Code executed successfully (no output)."

            if result.returncode != 0:
                return f"Error (Exit Code {result.returncode}):\n{output.strip()}"

            return output.strip()
            
        except subprocess.TimeoutExpired:
            return "Error: Execution timed out after 10 seconds."
        except Exception as e:
            return f"Error: {str(e)}"
