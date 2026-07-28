import os
import importlib
from fastapi.testclient import TestClient

def test_cors_no_env_var():
    # Ensure env var is not set
    if "CORS_ALLOWED_ORIGINS" in os.environ:
        del os.environ["CORS_ALLOWED_ORIGINS"]

    import agentblueprint_api.server
    importlib.reload(agentblueprint_api.server)

    client = TestClient(agentblueprint_api.server.app)

    response = client.options(
        "/workflows/run",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        }
    )
    # The server should reject or not allow the origin in its response header.
    assert "access-control-allow-origin" not in response.headers

def test_cors_with_env_var():
    os.environ["CORS_ALLOWED_ORIGINS"] = "http://localhost:3000, https://example.com"

    import agentblueprint_api.server
    importlib.reload(agentblueprint_api.server)

    client = TestClient(agentblueprint_api.server.app)

    response = client.options(
        "/workflows/run",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        }
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
