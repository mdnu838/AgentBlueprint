"""
Validation script for new tools (File & System).
"""
from agentblueprint_tools import FileReadTool, FileWriteTool, SystemTimeTool, SystemInfoTool
from pathlib import Path

def test_new_tools():
    print("\n🧪 Testing New Tools...")
    
    # 1. System Info
    sys_tool = SystemInfoTool()
    print(f"System Info: {sys_tool.run()}")
    
    # 2. Time
    time_tool = SystemTimeTool()
    print(f"Current Time: {time_tool.run()}")
    
    # 3. File Write
    write_tool = FileWriteTool()
    test_file = "test_tool_output.txt"
    res = write_tool.run(test_file, "Hello from Tool!")
    print(f"Write result: {res}")
    assert "Successfully wrote" in res
    
    # 4. File Read
    read_tool = FileReadTool()
    content = read_tool.run(test_file)
    print(f"Read content: {content}")
    assert "Hello from Tool!" in content
    
    # Cleanup
    Path(test_file).unlink()
    
    print("✅ New tools validation successful")

if __name__ == "__main__":
    test_new_tools()
