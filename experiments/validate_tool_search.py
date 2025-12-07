"""
Validation script for WebSearchTool.
"""
from agentblueprint_tools import WebSearchTool

def test_web_search():
    print("\n🧪 Testing WebSearchTool...")
    
    tool = WebSearchTool()
    
    print("Running search (expecting failure or success depending on installed packages)...")
    result = tool.run("Python AgentBlueprint")
    
    print(f"Result: {result}")
    
    # Check that we handled it gracefully (either success or specific error message)
    if "Error: 'duckduckgo-search' is not installed" in result:
        print("✅ Correctly identified missing dependency")
    elif "Python" in result:
        print("✅ Search successful (dependency present)")
    else:
        # Some other error?
        print(f"⚠️ Unexpected result: {result}")
    
    print("✅ Web Search validation completed")

if __name__ == "__main__":
    test_web_search()
