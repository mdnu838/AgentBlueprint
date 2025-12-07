"""
Validation script for Tool base class and ToolRegistry

Tests:
1. Tool class can be subclassed
2. Abstract methods are enforced
3. Tool metadata works correctly
4. Tool execution works
5. ToolRegistry registration and retrieval
6. ToolRegistry listing

Purpose: Test basic functionality before writing formal tests

Usage:
    python experiments/validate_tool_base.py
    
Expected Output:
    ✅ All validations passed!
"""


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
    
    print("   ✓ Tool subclass creation works")
    print("   ✓ Tool attributes accessible")
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
    result = calc.run(expression="2 + 2")
    assert result == 4, f"Expected 4, got {result}"
    
    result = calc.run(expression="10 * 5")
    assert result == 50, f"Expected 50, got {result}"
    
    print("   ✓ Tool execution returns correct results")
    print("   ✓ Tool accepts keyword arguments")
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
        print(f"   ✓ Correctly raised TypeError: {str(e)[:60]}...")
        print("✅ Abstract method enforcement works")


def test_tool_metadata():
    """Test tool metadata and to_dict conversion"""
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
    
    # Test to_dict
    tool_dict = tool.to_dict()
    assert tool_dict["name"] == "documented", "to_dict should include name"
    assert tool_dict["description"] == "A well-documented tool", "to_dict should include description"
    assert tool_dict["parameters"] is not None, "to_dict should include parameters"
    
    print("   ✓ Tool metadata accessible")
    print("   ✓ to_dict() serialization works")
    print("✅ Tool metadata works")


def test_tool_registry_registration():
    """Test registering tools in the registry"""
    print("\n🧪 Testing tool registration...")
    
    from agentblueprint_core.tools import Tool, ToolRegistry
    
    # Clear registry for clean test
    ToolRegistry.clear()
    
    class TestTool(Tool):
        name = "test_reg"
        description = "Test tool for registry"
        
        def run(self, input: str) -> str:
            return input
    
    # Register tool
    tool = TestTool()
    ToolRegistry.register(tool)
    
    # Retrieve tool
    retrieved = ToolRegistry.get("test_reg")
    assert retrieved is not None, "Tool should be retrievable"
    assert retrieved.name == "test_reg", "Retrieved tool should match"
    assert retrieved is tool, "Should retrieve same instance"
    
    print("   ✓ Tool registration works")
    print("   ✓ Tool retrieval works")
    print("✅ Tool registry registration works")


def test_tool_registry_listing():
    """Test listing all tools in registry"""
    print("\n🧪 Testing tool listing...")
    
    from agentblueprint_core.tools import Tool, ToolRegistry
    
    # Clear registry
    ToolRegistry.clear()
    
    class Tool1(Tool):
        name = "tool1"
        description = "First tool"
        def run(self, x): return x
    
    class Tool2(Tool):
        name = "tool2"
        description = "Second tool"
        def run(self, x): return x
    
    class Tool3(Tool):
        name = "tool3"
        description = "Third tool"
        def run(self, x): return x
    
    ToolRegistry.register(Tool1())
    ToolRegistry.register(Tool2())
    ToolRegistry.register(Tool3())
    
    tools = ToolRegistry.list_all()
    assert len(tools) == 3, f"Should have 3 tools, got {len(tools)}"
    
    tool_names = [t.name for t in tools]
    assert "tool1" in tool_names, "tool1 should be in registry"
    assert "tool2" in tool_names, "tool2 should be in registry"
    assert "tool3" in tool_names, "tool3 should be in registry"
    
    print("   ✓ list_all() returns all registered tools")
    print("   ✓ Tool count is accurate")
    print("✅ Tool registry listing works")


def test_tool_registry_missing():
    """Test behavior for missing tools"""
    print("\n🧪 Testing missing tool retrieval...")
    
    from agentblueprint_core.tools import ToolRegistry
    
    ToolRegistry.clear()
    
    # Try to get non-existent tool
    tool = ToolRegistry.get("nonexistent_tool")
    assert tool is None, "Should return None for missing tool"
    
    print("   ✓ Returns None for missing tool")
    print("✅ Missing tool handling works")


def test_tool_registry_clear():
    """Test clearing the registry"""
    print("\n🧪 Testing registry clear...")
    
    from agentblueprint_core.tools import Tool, ToolRegistry
    
    class DummyTool(Tool):
        name = "dummy"
        description = "Dummy"
        def run(self, x): return x
    
    ToolRegistry.register(DummyTool())
    assert len(ToolRegistry.list_all()) > 0, "Should have tools before clear"
    
    ToolRegistry.clear()
    assert len(ToolRegistry.list_all()) == 0, "Should have no tools after clear"
    
    print("   ✓ Registry clear works")
    print("✅ Registry clear functionality works")


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("Validating Tool Base Class and ToolRegistry")
    print("=" * 60)
    
    try:
        # Tool base class tests
        test_tool_subclass()
        test_tool_execution()
        test_abstract_enforcement()
        test_tool_metadata()
        
        # ToolRegistry tests
        test_tool_registry_registration()
        test_tool_registry_listing()
        test_tool_registry_missing()
        test_tool_registry_clear()
        
        print("\n" + "=" * 60)
        print("✅ All validations passed!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Write formal tests in packages/agentblueprint-core/tests/")
        print("  2. Update TASK_TRACKER.md status to ✅")
        print("  3. Commit changes to git")
        
    except AssertionError as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
