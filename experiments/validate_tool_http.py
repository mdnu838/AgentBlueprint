"""
Validation script for HTTPClientTool.
"""
from agentblueprint_tools import HTTPClientTool

def test_http_client():
    print("\n🧪 Testing HTTPClientTool...")
    
    # We shouldn't hit real external URLs in CI/automated tests generally, 
    # but for manual verification it's okay.
    # We can rely on httpbin.org or similar if we want reliability, or just mock it.
    # For this validation script, let's try a safe, reliable one like example.com
    
    client = HTTPClientTool()
    
    url = "https://www.example.com"
    print(f"Requesting {url}...")
    
    result = client.run(url)
    
    print(f"Result prefix: {result[:200]}...")
    
    assert "Status: 200" in result
    assert "Example Domain" in result
    
    print("✅ HTTP Client validation successful")

if __name__ == "__main__":
    test_http_client()
