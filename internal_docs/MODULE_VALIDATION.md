# Module Validation Guide

This document describes how to validate each module using the experiments folder before writing formal tests.

---

## 🎯 Validation Process

For each module implementation:

1. **Write the module** in the appropriate package
2. **Create validation script** in `experiments/`
3. **Run validation** and verify behavior
4. **Fix issues** if validation fails
5. **Write formal tests** in package `tests/`
6. **Update task tracker** status to ✅

---

## 📝 Validation Script Template

```python
# experiments/validate_<module_name>.py
"""
Validation script for <module_name>

Purpose: Test basic functionality of <module> before writing formal tests

Usage:
    python experiments/validate_<module_name>.py
    
Expected Output:
    ✅ All validations passed!
"""

def test_basic_functionality():
    """Test basic use case"""
    print("\n🧪 Testing basic functionality...")
    
    # Import the module
    from agentblueprint_core import ModuleName
    
    # Create instance
    instance = ModuleName(param1="value1")
    
    # Test basic operation
    result = instance.some_method()
    
    # Validate
    assert result is not None, "Result should not be None"
    assert isinstance(result, str), "Result should be string"
    
    print("✅ Basic functionality works")


def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n🧪 Testing edge cases...")
    
    # Test with empty input
    # Test with invalid input
    # Test with boundary conditions
    
    print("✅ Edge cases handled correctly")


def test_integration():
    """Test integration with other components"""
    print("\n🧪 Testing integration...")
    
    # Test how this module works with others
    
    print("✅ Integration works")


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("Validating <module_name>")
    print("=" * 60)
    
    try:
        test_basic_functionality()
        test_edge_cases()
        test_integration()
        
        print("\n" + "=" * 60)
        print("✅ All validations passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Validation failed: {e}")
        raise
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
```

---

## 📚 Example Validation Scripts

### Example 1: Validating Tool Base Class

```python
# experiments/validate_tool_base.py
"""
Validation script for Tool base class

Tests:
1. Tool class can be subclassed
2. Abstract methods are enforced
3. Tool metadata works correctly
4. Tool execution works
"""

from abc import ABC, abstractmethod


def test_tool_subclass():
    """Test that Tool can be subclassed"""
    print("\n🧪 Testing Tool subclass...")
    
    from agentblueprint_core.tools import Tool
    
    class TestTool(Tool):
        name = "test_tool"
        description = "A test tool"
        
        def run(self, input_data: str) -> str:
            return f"Processed: {input_data}"
    
    tool = TestTool()
    assert tool.name == "test_tool", "Tool name should match"
    assert tool.description == "A test tool", "Tool description should match"
    
    print("✅ Tool subclass works")


def test_tool_execution():
    """Test tool execution"""
    print("\n🧪 Testing tool execution...")
    
    from agentblueprint_core.tools import Tool
    
    class CalculatorTool(Tool):
        name = "calculator"
        description = "Simple calculator"
        
        def run(self, expression: str) -> float:
            # Simple eval for testing (use safe_eval in production)
            return eval(expression)
    
    calc = CalculatorTool()
    result = calc.run("2 + 2")
    assert result == 4, f"Expected 4, got {result}"
    
    result = calc.run("10 * 5")
    assert result == 50, f"Expected 50, got {result}"
    
    print("✅ Tool execution works")


def test_abstract_enforcement():
    """Test that abstract methods are enforced"""
    print("\n🧪 Testing abstract method enforcement...")
    
    from agentblueprint_core.tools import Tool
    
    try:
        class IncompleteTool(Tool):
            name = "incomplete"
            description = "Incomplete tool"
            # Missing run() method
        
        # This should raise TypeError
        tool = IncompleteTool()
        assert False, "Should have raised TypeError for missing run() method"
        
    except TypeError as e:
        print(f"   Correctly raised TypeError: {e}")
        print("✅ Abstract method enforcement works")


def test_tool_metadata():
    """Test tool metadata and introspection"""
    print("\n🧪 Testing tool metadata...")
    
    from agentblueprint_core.tools import Tool
    
    class DocumentedTool(Tool):
        name = "documented"
        description = "A well-documented tool"
        parameters = {
            "input": {"type": "string", "description": "Input text"}
        }
        
        def run(self, input: str) -> str:
            return input.upper()
    
    tool = DocumentedTool()
    assert hasattr(tool, 'name'), "Tool should have name"
    assert hasattr(tool, 'description'), "Tool should have description"
    assert hasattr(tool, 'parameters'), "Tool should have parameters"
    
    print("✅ Tool metadata works")


def main():
    print("=" * 60)
    print("Validating Tool Base Class")
    print("=" * 60)
    
    try:
        test_tool_subclass()
        test_tool_execution()
        test_abstract_enforcement()
        test_tool_metadata()
        
        print("\n" + "=" * 60)
        print("✅ All validations passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        raise


if __name__ == "__main__":
    main()
```

---

### Example 2: Validating Agent Class

```python
# experiments/validate_agent.py
"""
Validation script for Agent class

Tests:
1. Agent initialization
2. Agent with tools
3. Agent conversation flow
4. Agent with different models
"""


def test_agent_init():
    """Test agent initialization"""
    print("\n🧪 Testing agent initialization...")
    
    from agentblueprint_core import Agent
    
    agent = Agent(
        name="test_agent",
        model="openai:gpt-4",
        system_prompt="You are a test agent"
    )
    
    assert agent.name == "test_agent", "Agent name should match"
    assert agent.model == "openai:gpt-4", "Agent model should match"
    assert agent.system_prompt == "You are a test agent", "System prompt should match"
    
    print("✅ Agent initialization works")


def test_agent_with_tools():
    """Test agent with tools"""
    print("\n🧪 Testing agent with tools...")
    
    from agentblueprint_core import Agent, Tool
    
    class EchoTool(Tool):
        name = "echo"
        description = "Echoes input"
        
        def run(self, text: str) -> str:
            return f"Echo: {text}"
    
    class ReverseTool(Tool):
        name = "reverse"
        description = "Reverses input"
        
        def run(self, text: str) -> str:
            return text[::-1]
    
    agent = Agent(
        name="tool_agent",
        model="openai:gpt-4",
        tools=[EchoTool(), ReverseTool()]
    )
    
    assert len(agent.tools) == 2, "Agent should have 2 tools"
    assert agent.tools[0].name == "echo", "First tool should be echo"
    assert agent.tools[1].name == "reverse", "Second tool should be reverse"
    
    print("✅ Agent with tools works")


def test_agent_tool_execution():
    """Test that agent can execute tools"""
    print("\n🧪 Testing agent tool execution...")
    
    from agentblueprint_core import Agent, Tool
    
    class CalculatorTool(Tool):
        name = "calculator"
        description = "Simple calculator"
        
        def run(self, expression: str) -> float:
            return eval(expression)
    
    agent = Agent(
        name="calc_agent",
        model="mock:test",
        tools=[CalculatorTool()]
    )
    
    # Agent should be able to access and execute tools
    calc_tool = agent.tools[0]
    result = calc_tool.run("5 + 3")
    assert result == 8, f"Expected 8, got {result}"
    
    print("✅ Agent tool execution works")


def test_agent_configuration():
    """Test agent configuration options"""
    print("\n🧪 Testing agent configuration...")
    
    from agentblueprint_core import Agent
    
    agent = Agent(
        name="configured_agent",
        model="openai:gpt-4",
        system_prompt="Test",
        temperature=0.7,
        max_tokens=1000
    )
    
    assert agent.temperature == 0.7, "Temperature should be configurable"
    assert agent.max_tokens == 1000, "Max tokens should be configurable"
    
    print("✅ Agent configuration works")


def main():
    print("=" * 60)
    print("Validating Agent Class")
    print("=" * 60)
    
    try:
        test_agent_init()
        test_agent_with_tools()
        test_agent_tool_execution()
        test_agent_configuration()
        
        print("\n" + "=" * 60)
        print("✅ All validations passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
```

---

### Example 3: Validating ToolRegistry

```python
# experiments/validate_tool_registry.py
"""
Validation script for ToolRegistry

Tests:
1. Tool registration
2. Tool retrieval
3. Tool listing
4. Duplicate handling
"""


def test_tool_registration():
    """Test registering tools"""
    print("\n🧪 Testing tool registration...")
    
    from agentblueprint_core import Tool, ToolRegistry
    
    class TestTool(Tool):
        name = "test"
        description = "Test tool"
        
        def run(self, input: str) -> str:
            return input
    
    # Register tool
    tool = TestTool()
    ToolRegistry.register(tool)
    
    # Retrieve tool
    retrieved = ToolRegistry.get("test")
    assert retrieved is not None, "Tool should be retrievable"
    assert retrieved.name == "test", "Retrieved tool should match"
    
    print("✅ Tool registration works")


def test_tool_listing():
    """Test listing all tools"""
    print("\n🧪 Testing tool listing...")
    
    from agentblueprint_core import Tool, ToolRegistry
    
    class Tool1(Tool):
        name = "tool1"
        description = "First tool"
        def run(self, x): return x
    
    class Tool2(Tool):
        name = "tool2"
        description = "Second tool"
        def run(self, x): return x
    
    # Clear registry (if method exists)
    if hasattr(ToolRegistry, 'clear'):
        ToolRegistry.clear()
    
    ToolRegistry.register(Tool1())
    ToolRegistry.register(Tool2())
    
    tools = ToolRegistry.list_all()
    assert len(tools) >= 2, "Should have at least 2 tools"
    
    tool_names = [t.name for t in tools]
    assert "tool1" in tool_names, "tool1 should be in registry"
    assert "tool2" in tool_names, "tool2 should be in registry"
    
    print("✅ Tool listing works")


def test_tool_retrieval_errors():
    """Test error handling for missing tools"""
    print("\n🧪 Testing tool retrieval errors...")
    
    from agentblueprint_core import ToolRegistry
    
    try:
        # Try to get non-existent tool
        tool = ToolRegistry.get("nonexistent_tool")
        
        if tool is None:
            print("   Returns None for missing tool")
        else:
            assert False, "Should return None or raise error for missing tool"
            
    except KeyError:
        print("   Raises KeyError for missing tool")
    
    print("✅ Tool retrieval error handling works")


def main():
    print("=" * 60)
    print("Validating ToolRegistry")
    print("=" * 60)
    
    try:
        test_tool_registration()
        test_tool_listing()
        test_tool_retrieval_errors()
        
        print("\n" + "=" * 60)
        print("✅ All validations passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
```

---

## 🔄 Running Validations

### Single Validation

```bash
cd /Users/nizamuddin/Documents/Project/AgentBlueprint
python experiments/validate_tool_base.py
```

### All Validations

Create a runner script:

```python
# experiments/run_all_validations.py
"""
Run all validation scripts in experiments folder
"""

import subprocess
import sys
from pathlib import Path


def run_validation(script_path: Path) -> tuple[bool, str]:
    """Run a validation script and return (success, output)"""
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"{e.stdout}\n{e.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Timeout exceeded (30s)"


def main():
    experiments_dir = Path(__file__).parent
    validation_scripts = sorted(experiments_dir.glob("validate_*.py"))
    
    if not validation_scripts:
        print("No validation scripts found!")
        return 1
    
    print("=" * 70)
    print(f"Running {len(validation_scripts)} validation scripts")
    print("=" * 70)
    
    passed = []
    failed = []
    
    for script in validation_scripts:
        print(f"\n▶️  {script.name}")
        print("-" * 70)
        
        success, output = run_validation(script)
        
        if success:
            print(output)
            passed.append(script.name)
        else:
            print(output)
            failed.append(script.name)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Passed: {len(passed)}")
    print(f"❌ Failed: {len(failed)}")
    
    if passed:
        print("\n✅ Passed scripts:")
        for name in passed:
            print(f"   - {name}")
    
    if failed:
        print("\n❌ Failed scripts:")
        for name in failed:
            print(f"   - {name}")
    
    print("=" * 70)
    
    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

Run all validations:

```bash
python experiments/run_all_validations.py
```

---

## ✅ Validation Checklist

Before marking a module as complete, ensure:

- [ ] Validation script created in `experiments/`
- [ ] Validation script has clear docstring
- [ ] Tests basic functionality
- [ ] Tests edge cases
- [ ] Tests error handling
- [ ] Tests integration (if applicable)
- [ ] Prints clear success/failure messages
- [ ] Can be run standalone
- [ ] Added to validation runner
- [ ] All validations pass
- [ ] Formal tests written in package `tests/`
- [ ] Task status updated in TASK_TRACKER.md

---

## 🎓 Best Practices

### DO ✅

- **Keep validations simple** - Focus on core functionality
- **Test one thing at a time** - Separate tests for each feature
- **Print clear messages** - Show what's being tested
- **Use assertions** - Make expectations explicit
- **Handle errors gracefully** - Catch and report errors clearly

### DON'T ❌

- **Don't make validations too complex** - Save complex tests for formal tests
- **Don't skip edge cases** - They often reveal bugs
- **Don't assume** - Validate all assumptions
- **Don't leave failed validations** - Fix immediately or mark as blocked
- **Don't forget to update status** - Keep TASK_TRACKER current

---

## 📝 Moving to Formal Tests

Once validation passes:

1. **Copy validation logic** to formal pytest test
2. **Add more comprehensive test cases**
3. **Add fixtures** for reusable test data
4. **Add parametrization** for multiple inputs
5. **Add test documentation**
6. **Consider keeping or archiving** validation script

### Example Transition

**Validation Script:**
```python
def test_tool_execution():
    calc = CalculatorTool()
    result = calc.run("2 + 2")
    assert result == 4
```

**Formal Test:**
```python
import pytest
from agentblueprint_core.tools import Tool

class TestCalculatorTool:
    """Comprehensive tests for CalculatorTool"""
    
    @pytest.fixture
    def calc_tool(self):
        """Create a CalculatorTool instance"""
        class CalculatorTool(Tool):
            name = "calculator"
            description = "Simple calculator"
            
            def run(self, expression: str) -> float:
                return eval(expression)
        
        return CalculatorTool()
    
    @pytest.mark.parametrize("expression,expected", [
        ("2 + 2", 4),
        ("10 - 5", 5),
        ("3 * 4", 12),
        ("15 / 3", 5),
        ("2 ** 3", 8),
    ])
    def test_calculations(self, calc_tool, expression, expected):
        """Test various calculations"""
        result = calc_tool.run(expression)
        assert result == expected
    
    def test_invalid_expression(self, calc_tool):
        """Test error handling for invalid expressions"""
        with pytest.raises(SyntaxError):
            calc_tool.run("invalid expression")
```

---

**Last Updated:** 26 November 2025
