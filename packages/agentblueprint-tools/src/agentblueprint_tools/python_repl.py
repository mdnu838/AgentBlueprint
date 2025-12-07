"""
Python REPL tool for executing code.
"""
import sys
from io import StringIO
from typing import Optional
from agentblueprint_core import Tool

class PythonREPLTool(Tool):
    """
    A tool for running Python code.
    WARNING: This executes code locally and is not sandboxed. Use with caution.
    """
    name = "python_repl"
    description = "Executes Python code and returns stdout/stderr. Input should be valid python code."
    
    def run(self, code: str) -> str:
        """Execute the python code and return the output."""
        # Capture stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = StringIO()
        
        try:
            sys.stdout = redirected_output
            sys.stderr = redirected_output
            
            # Create a shared local scope for persistence if needed, 
            # but for now we treat each run as isolated or we could use a class-level dict
            # For simplicity: isolated
            local_scope = {}
            
            exec(code, {}, local_scope)
            
            output = redirected_output.getvalue()
            if not output:
                return "Code executed successfully (no output)."
            return output
            
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
