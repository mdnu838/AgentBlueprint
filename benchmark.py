import time
import urllib.request
from unittest.mock import patch
from agentblueprint_tools import generate_tools_from_openapi

mock_schema = {
  "openapi": "3.0.0",
  "info": {"title": "Sample API", "version": "1.0.0"},
  "servers": [{"url": "https://api.example.com"}],
  "paths": {
    "/users": {
      "get": {
        "summary": "List users",
        "operationId": "listUsers",
        "parameters": []
      }
    }
  }
}

import json

# Mock urlopen to simulate network latency
class MockResponse:
    def __init__(self, content):
        self.content = content
    def read(self):
        return self.content
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass

def mock_urlopen(url):
    time.sleep(0.1)  # simulate 100ms latency
    return MockResponse(json.dumps(mock_schema).encode('utf-8'))

with patch('urllib.request.urlopen', mock_urlopen):
    start = time.time()
    for _ in range(10):
        generate_tools_from_openapi("http://example.com/schema.json")
    end = time.time()
    print(f"Time taken: {end - start:.4f} seconds")
