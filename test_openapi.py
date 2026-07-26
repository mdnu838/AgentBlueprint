import json
from agentblueprint_tools import generate_tools_from_openapi

mock_schema = {
  "openapi": "3.0.0",
  "info": {
    "title": "Sample API",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://api.example.com"
    }
  ],
  "paths": {
    "/users": {
      "get": {
        "summary": "List users",
        "operationId": "listUsers",
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "required": False,
            "schema": {
              "type": "integer"
            }
          }
        ]
      }
    }
  }
}

tools = generate_tools_from_openapi(mock_schema)
for t in tools:
    print(f"Tool Name: {t.name}")
    print(f"Description: {t.description}")
    print(f"Parameters: {t.parameters}")
