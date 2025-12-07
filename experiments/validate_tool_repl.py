"""
Validation script for PythonREPLTool.
"""
from agentblueprint_tools import PythonREPLTool

def test_repl():
    print("\n🧪 Testing PythonREPLTool...")
    
    repl = PythonREPLTool()
    
    # Test basic print
    code = "print('Hello REPL')"
    result = repl.run(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    assert "Hello REPL" in result
    
    # Test math
    code = "print(2 + 2)"
    result = repl.run(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    assert "4" in result
    
    # Test error
    code = "print(1/0)"
    result = repl.run(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    assert "division by zero" in result
    
    print("✅ REPL validation successful")

if __name__ == "__main__":
    test_repl()
