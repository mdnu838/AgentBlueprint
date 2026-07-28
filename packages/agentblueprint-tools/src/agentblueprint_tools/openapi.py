"""
OpenAPI to Tool generator for AgentBlueprint.

This module provides functionality to parse an OpenAPI 3.x schema
and dynamically generate `Tool` classes for each defined operation.
"""

import json
import logging
import urllib.parse
from typing import Any, Dict, List, Optional, Union
import yaml
import httpx

from agentblueprint_core import Tool

logger = logging.getLogger(__name__)

# Shared HTTP client for connection pooling and Keep-Alive benefits
_http_client = httpx.Client(timeout=15.0, follow_redirects=True)


class OpenAPIOperationTool(Tool):
    """
    A tool that wraps a specific OpenAPI operation (HTTP endpoint).
    """

    def __init__(self, operation_id: str, method: str, path: str, base_url: str, description: str, parameters_schema: dict):
        self.name = operation_id
        self.description = description
        self.parameters = parameters_schema
        self._method = method.upper()
        self._path = path
        self._base_url = base_url.rstrip("/")

    def run(self, **kwargs) -> Any:
        """
        Execute the HTTP request for the OpenAPI operation.
        """
        url_path = self._path
        query_params = {}
        headers = {"Content-Type": "application/json"}
        body_data = None

        # Basic mapping of kwargs to path/query/body
        # Note: A fully robust implementation would parse the original OpenAPI
        # schema for 'in: path', 'in: query', etc. For this basic implementation,
        # we do a simple heuristic:
        for key, value in kwargs.items():
            if f"{{{key}}}" in url_path:
                url_path = url_path.replace(f"{{{key}}}", urllib.parse.quote(str(value)))
            elif self._method in ["POST", "PUT", "PATCH"]:
                if body_data is None:
                    body_data = {}
                body_data[key] = value
            else:
                query_params[key] = value

        url = f"{self._base_url}{url_path}"

        request_kwargs = {
            "method": self._method,
            "url": url,
            "headers": headers,
        }

        if query_params:
            request_kwargs["params"] = query_params

        if body_data is not None:
            request_kwargs["json"] = body_data

        try:
            response = _http_client.request(**request_kwargs)
            response.raise_for_status()
            resp_body = response.text
            try:
                return json.loads(resp_body)
            except json.JSONDecodeError:
                return resp_body
        except httpx.HTTPStatusError as e:
            return f"HTTP Error {e.response.status_code}: {e.response.text}"
        except httpx.RequestError as e:
            return f"URL Error: {str(e)}"
        except Exception as e:
            return f"Error executing request: {str(e)}"


def generate_tools_from_openapi(schema: Union[str, Dict[str, Any]]) -> List[Tool]:
    """
    Parse an OpenAPI schema and generate Tools.

    Args:
        schema: Can be a URL (str), file path (str), or a parsed dictionary.

    Returns:
        List of generated Tools.
    """
    spec = None

    if isinstance(schema, str):
        if schema.startswith("http://") or schema.startswith("https://"):
            try:
                response = _http_client.get(schema)
                response.raise_for_status()
                content = response.text
                if schema.endswith(".yaml") or schema.endswith(".yml"):
                    spec = yaml.safe_load(content)
                else:
                    spec = json.loads(content)
            except Exception as e:
                logger.error(f"Failed to load OpenAPI schema from URL {schema}: {e}")
                return []
        else:
            try:
                with open(schema, "r") as f:
                    if schema.endswith(".yaml") or schema.endswith(".yml"):
                        spec = yaml.safe_load(f)
                    else:
                        spec = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load OpenAPI schema from file {schema}: {e}")
                return []
    elif isinstance(schema, dict):
        spec = schema
    else:
        logger.error("Schema must be a URL, file path, or dictionary.")
        return []

    if not spec:
        return []

    servers = spec.get("servers", [{"url": ""}])
    base_url = servers[0].get("url", "")

    tools = []
    paths = spec.get("paths", {})

    for path, methods in paths.items():
        for method, operation in methods.items():
            if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                continue

            # Generate operation ID if not present
            operation_id = operation.get("operationId")
            if not operation_id:
                # E.g., GET /users/{id} -> get_users_id
                clean_path = path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
                operation_id = f"{method}_{clean_path}"

            description = operation.get("summary", operation.get("description", f"{method.upper()} {path}"))

            # Build a simple parameters schema
            parameters_schema = {
                "type": "object",
                "properties": {},
                "required": []
            }

            for param in operation.get("parameters", []):
                name = param.get("name")
                if not name:
                    continue
                param_schema = param.get("schema", {"type": "string"})
                parameters_schema["properties"][name] = {
                    "type": param_schema.get("type", "string"),
                    "description": param.get("description", "")
                }
                if param.get("required"):
                    parameters_schema["required"].append(name)

            # Simple body handling for POST/PUT
            request_body = operation.get("requestBody")
            if request_body:
                content = request_body.get("content", {})
                json_content = content.get("application/json", {})
                body_schema = json_content.get("schema", {})

                if body_schema.get("type") == "object" and "properties" in body_schema:
                    for prop_name, prop_details in body_schema["properties"].items():
                         parameters_schema["properties"][prop_name] = prop_details
                    if "required" in body_schema:
                         parameters_schema["required"].extend(body_schema["required"])

            # Clean up empty required list
            if not parameters_schema["required"]:
                del parameters_schema["required"]

            tool = OpenAPIOperationTool(
                operation_id=operation_id,
                method=method,
                path=path,
                base_url=base_url,
                description=description,
                parameters_schema=parameters_schema
            )
            tools.append(tool)

    return tools
