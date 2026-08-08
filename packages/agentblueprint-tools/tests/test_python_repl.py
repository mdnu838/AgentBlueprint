import os
from agentblueprint_tools.python_repl import PythonREPLTool

def test_python_repl_basic():
    tool = PythonREPLTool()
    code = "print('hello world')"
    result = tool.run(code)
    assert result == "hello world"

def test_python_repl_error():
    tool = PythonREPLTool()
    code = "1 / 0"
    result = tool.run(code)
    assert "ZeroDivisionError" in result
    assert "Error (Exit Code 1):" in result

def test_python_repl_no_output():
    tool = PythonREPLTool()
    code = "x = 5"
    result = tool.run(code)
    assert result == "Code executed successfully (no output)."

def test_python_repl_environment_isolation():
    # Set a secret in the parent process environment
    os.environ["SUPER_SECRET_TOKEN"] = "this-is-a-secret-do-not-leak"

    tool = PythonREPLTool()
    code = "import os; print(os.environ.get('SUPER_SECRET_TOKEN', 'not found'))"
    result = tool.run(code)

    # Clean up environment
    del os.environ["SUPER_SECRET_TOKEN"]

    # The subprocess should not be able to read the token since we pass env={}
    assert result == "not found"
